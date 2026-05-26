from datetime import datetime
from typing import Dict, List, NamedTuple, Optional, Tuple
import argparse
import sys
import time

from .dtos import MonitorConfig, ServerConfig
from .enums import ServerStatus
from .repositories import (
    monitor_config_repository,
    monitor_list_repository,
    servers_config_repository,
    user_info_repository,
)
from .services import connectivity_service, log_service, notification_service


_ServerStatusByHostname = Dict[str, ServerStatus]

_CycleResult = NamedTuple(
    "_CycleResult",
    [
        ("statuses", _ServerStatusByHostname),
        ("last_notification_at", Optional[datetime]),
    ]
)

_StatusDiff = NamedTuple(
    "_StatusDiff",
    [
        ("new_offline", List[ServerConfig]),
        ("recovered", List[ServerConfig]),
        ("still_offline", List[ServerConfig]),
    ]
)


def _print_banner() -> None:
    art = [
        r"   ____    _    __  __ ",
        r"  / ___|  / \  |  \/  |",
        r"  \___ \ / _ \ | |\/| |",
        r"   ___) / ___ \| |  | |",
        r"  |____/_/   \_\_|  |_|",
    ]
    title = "  [S]erver [A]vailability [M]onitor"
    notice = "  ( ! ) Output is being logged in paths.logs_folder"

    art_width = max(len(line) for line in art)
    w = max(len(title), len(notice), art_width) + 2
    art_pad = " " * ((w - art_width) // 2)
    rule = "─" * w

    print()
    print(f"  ╭{rule}╮")
    for line in art:
        print(f"  │{art_pad + line:<{w}}│")
    print(f"  │{'':^{w}}│")
    print(f"  │{title:^{w}}│")
    print(f"  │{'':^{w}}│")
    print(f"  │{notice:<{w}}│")
    print(f"  │{'':^{w}}│")
    print(f"  ╰{rule}╯")
    print()


def _parse_args() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(description="Server Availability Monitor")
    parser.add_argument(
        "-l", "--list",
        dest="monitor_list_file",
        default="monitor_list.txt",
        help="Path to the monitor list file (default: monitor_list.txt)",
    )
    parser.add_argument(
        "-c", "--config",
        dest="monitor_config_file",
        default="monitorConfig.json",
        help="Path to the monitor config file (default: monitorConfig.json)",
    )
    args = parser.parse_args()
    return args.monitor_list_file, args.monitor_config_file


def _bootstrap(monitor_list_file: str, monitor_config_file: str) -> None:
    monitor_config = monitor_config_repository.load(monitor_config_file)
    is_valid, errors = monitor_config.validate()

    if not is_valid:
        print(f"ERROR: invalid monitor config: {errors}", file=sys.stderr)
        sys.exit(1)

    log_service.setup(monitor_config.paths.logs_folder)
    _print_banner()
    log_service.emit_info("monitor started, list=%s", monitor_list_file)


def _reload_configs(
    monitor_list_file: str,
    monitor_config_file: str,
    last_valid_monitor_config: Optional[MonitorConfig],
) -> Optional[MonitorConfig]:
    def reload_monitor_config() -> None:
        nonlocal last_valid_monitor_config
        try:
            config = monitor_config_repository.load(monitor_config_file)
            is_valid, errors = config.validate()
            if not is_valid:
                log_service.emit_error("invalid monitor config, keeping last valid: %s", errors)
                return

            last_valid_monitor_config = config
        except Exception as error:
            log_service.emit_error("failed to reload monitor config, keeping last valid: %s", error)

    def reload_user_infos() -> None:
        try:
            user_infos = user_info_repository.load(last_valid_monitor_config.paths.user_info_file)
            for user_info in user_infos:
                is_valid, errors = user_info.validate()
                if not is_valid:
                    log_service.emit_warning("invalid user_info skipped: %s", errors)
        except Exception as error:
            log_service.emit_error("failed to reload user_info: %s", error)

    def reload_server_configs() -> None:
        try:
            server_configs = servers_config_repository.load(
                last_valid_monitor_config.paths.servers_config_file
            )
            for server_config in server_configs:
                is_valid, errors = server_config.validate()
                if not is_valid:
                    log_service.emit_warning("invalid server_config skipped: %s", errors)
        except Exception as error:
            log_service.emit_error("failed to reload servers_config: %s", error)

    def reload_monitor_list() -> None:
        try:
            monitor_list_repository.load(monitor_list_file)
        except Exception as error:
            log_service.emit_error("failed to reload monitor_list: %s", error)

    reload_monitor_config()
    reload_user_infos()
    reload_server_configs()
    reload_monitor_list()

    return last_valid_monitor_config


def _run_cycle(
    monitor_config: MonitorConfig,
    previous_statuses: _ServerStatusByHostname,
    last_notification_at: Optional[datetime],
) -> _CycleResult:
    def check_servers() -> _ServerStatusByHostname:
        hostnames = monitor_list_repository.get_all()

        server_configs = [
            s for hostname in hostnames
            if (s := servers_config_repository.get_by_hostname(hostname)) is not None
        ]

        return {
            s.hostname: connectivity_service.check(
                s,
                monitor_config.timing.check_timeout_in_seconds
            )
            for s in server_configs
        }

    def send_notifications(diff: _StatusDiff) -> Optional[datetime]:
        notified_at = last_notification_at
        user_infos = [u for u in user_info_repository.get_all() if u.validate()[0]]

        try:
            if diff.new_offline:
                notification_service.notify_offline(
                    diff.new_offline,
                    user_infos,
                    monitor_config.smtp
                )
                notified_at = datetime.now()

            if diff.recovered:
                notification_service.notify_recovery(
                    diff.recovered,
                    diff.still_offline,
                    user_infos,
                    monitor_config.smtp,
                )
                notified_at = datetime.now()

            reminder_due = diff.still_offline and _is_reminder_due(
                notified_at, monitor_config.timing.notification_interval_in_seconds
            )

            if reminder_due:
                notification_service.notify_reminder(
                    diff.still_offline,
                    user_infos,
                    monitor_config.smtp
                )
                notified_at = datetime.now()
        except Exception as error:
            log_service.emit_error("failed to send notification: %s", error)

        return notified_at

    current_statuses = check_servers()
    diff = _diff_statuses(previous_statuses, current_statuses)
    last_notification_at = send_notifications(diff)

    return _CycleResult(current_statuses, last_notification_at)


def _diff_statuses(
    previous_statuses: _ServerStatusByHostname,
    current_statuses: _ServerStatusByHostname,
) -> _StatusDiff:
    new_offline, recovered, still_offline = [], [], []

    def classify(hostname: str, status: ServerStatus) -> None:
        server_config = servers_config_repository.get_by_hostname(hostname)
        if not server_config:
            return

        previous = previous_statuses.get(hostname, ServerStatus.ONLINE)

        is_offline = status == ServerStatus.OFFLINE
        was_offline = previous == ServerStatus.OFFLINE

        if is_offline:
            still_offline.append(server_config)

        if is_offline and not was_offline:
            new_offline.append(server_config)

        if not is_offline and was_offline:
            recovered.append(server_config)

    for hostname, status in current_statuses.items():
        classify(hostname, status)

    return _StatusDiff(new_offline, recovered, still_offline)


def _is_reminder_due(
    last_notification_at: Optional[datetime],
    interval_in_seconds: int,
) -> bool:
    if last_notification_at is None:
        return True
    return (datetime.now() - last_notification_at).total_seconds() >= interval_in_seconds


if __name__ == "__main__":
    monitor_list_file, monitor_config_file = _parse_args()
    _bootstrap(monitor_list_file, monitor_config_file)

    previous_statuses = {}
    last_notification_at = None
    last_valid_monitor_config = None

    try:
        while True:
            last_valid_monitor_config = _reload_configs(
                monitor_list_file,
                monitor_config_file,
                last_valid_monitor_config,
            )
            result = _run_cycle(last_valid_monitor_config, previous_statuses, last_notification_at)
            previous_statuses = result.statuses
            last_notification_at = result.last_notification_at
            time.sleep(last_valid_monitor_config.timing.check_interval_in_seconds)
    except KeyboardInterrupt:
        log_service.emit_info("monitor stopped by user")
