import argparse
import sys
import time
from datetime import datetime
from typing import NamedTuple, Optional

from app.dtos import MonitorConfig, ServerConfig
from app.enums import ServerStatus
from app.repositories import (
    monitor_config_repository,
    monitor_list_repository,
    servers_config_repository,
    user_info_repository,
)
from app.services import connectivity_service, log_service, notification_service
from app.types import ServerStatusByHostname


_MONITOR_CONFIG_FILE = "monitorConfig.json"
_last_valid_monitor_config = None

logger = log_service.get_instance(__name__)


class StatusDiff(NamedTuple):
    new_offline: list[ServerConfig]
    recovered: list[ServerConfig]
    still_offline: list[ServerConfig]


class CycleResult(NamedTuple):
    statuses: ServerStatusByHostname
    last_notification_at: Optional[datetime]


def main() -> None:
    parser = argparse.ArgumentParser(description="Server Availability Monitor")
    parser.add_argument(
        "monitor_list_path",
        nargs="?",
        default="monitor_list.txt",
        help="Path to the monitor list file (default: monitor_list.txt)",
    )
    args = parser.parse_args()

    _bootstrap(args.monitor_list_path)

    previous_statuses = {}
    last_notification_at = None

    try:
        while True:
            monitor_config = _reload_configs(args.monitor_list_path)
            result = _run_cycle(monitor_config, previous_statuses, last_notification_at)
            previous_statuses = result.statuses
            last_notification_at = result.last_notification_at
            time.sleep(monitor_config.timing.check_interval_in_seconds)
    except KeyboardInterrupt:
        logger.info("monitor stopped by user")


def _bootstrap(monitor_list_path: str) -> None:
    monitor_config = monitor_config_repository.load(_MONITOR_CONFIG_FILE)
    is_valid, errors = monitor_config.validate()
    if not is_valid:
        print(f"ERROR: invalid monitor config: {errors}", file=sys.stderr)
        sys.exit(1)

    log_service.setup(monitor_config.paths.logs_folder)
    logger.info("monitor started, list=%s", monitor_list_path)


def _reload_configs(monitor_list_path: str) -> MonitorConfig:
    global _last_valid_monitor_config

    try:
        monitor_config = monitor_config_repository.load(_MONITOR_CONFIG_FILE)
        is_valid, errors = monitor_config.validate()
        if is_valid:
            _last_valid_monitor_config = monitor_config
        else:
            logger.error("invalid monitor config, keeping last valid: %s", errors)
    except Exception as error:
        logger.error("failed to reload monitor config, keeping last valid: %s", error)

    monitor_config = _last_valid_monitor_config

    try:
        user_infos = user_info_repository.load(monitor_config.paths.user_info_file)
        for user_info in user_infos:
            is_valid, errors = user_info.validate()
            if not is_valid:
                logger.warning("invalid user_info skipped: %s", errors)
    except Exception as error:
        logger.error("failed to reload user_info: %s", error)

    try:
        server_configs = servers_config_repository.load(monitor_config.paths.servers_config_file)
        for server_config in server_configs:
            is_valid, errors = server_config.validate()
            if not is_valid:
                logger.warning("invalid server_config skipped: %s", errors)
    except Exception as error:
        logger.error("failed to reload servers_config: %s", error)

    try:
        monitor_list_repository.load(monitor_list_path)
    except Exception as error:
        logger.error("failed to reload monitor_list: %s", error)

    return monitor_config


def _run_cycle(
    monitor_config: MonitorConfig,
    previous_statuses: ServerStatusByHostname,
    last_notification_at: Optional[datetime],
) -> CycleResult:
    hostnames = monitor_list_repository.get_all()
    server_configs = [
        s for hostname in hostnames
        if (s := servers_config_repository.get_by_hostname(hostname)) is not None
    ]

    current_statuses = {
        s.hostname: connectivity_service.check(s, monitor_config.timing.check_timeout_in_seconds)
        for s in server_configs
    }

    diff = _diff_statuses(previous_statuses, current_statuses)
    user_infos = [u for u in user_info_repository.get_all() if u.validate()[0]]

    try:
        if diff.new_offline:
            notification_service.notify_offline(diff.new_offline, user_infos, monitor_config.smtp)
            last_notification_at = datetime.now()

        if diff.recovered:
            notification_service.notify_recovery(
                diff.recovered, diff.still_offline, user_infos, monitor_config.smtp
            )
            last_notification_at = datetime.now()

        if diff.still_offline and _is_reminder_due(
            last_notification_at, monitor_config.timing.notification_interval_in_seconds
        ):
            notification_service.notify_reminder(diff.still_offline, user_infos, monitor_config.smtp)
            last_notification_at = datetime.now()
    except Exception as error:
        logger.error("failed to send notification: %s", error)

    return CycleResult(current_statuses, last_notification_at)


def _diff_statuses(
    previous_statuses: ServerStatusByHostname,
    current_statuses: ServerStatusByHostname,
) -> StatusDiff:
    new_offline, recovered, still_offline = [], [], []

    for hostname, status in current_statuses.items():
        previous = previous_statuses.get(hostname, ServerStatus.ONLINE)
        server_config = servers_config_repository.get_by_hostname(hostname)

        if server_config is None:
            continue

        if status == ServerStatus.OFFLINE:
            still_offline.append(server_config)
            if previous == ServerStatus.ONLINE:
                new_offline.append(server_config)
        elif status == ServerStatus.ONLINE and previous == ServerStatus.OFFLINE:
            recovered.append(server_config)

    return StatusDiff(new_offline, recovered, still_offline)


def _is_reminder_due(
    last_notification_at: Optional[datetime],
    interval_in_seconds: int,
) -> bool:
    if last_notification_at is None:
        return True
    return (datetime.now() - last_notification_at).total_seconds() >= interval_in_seconds


if __name__ == "__main__":
    main()
