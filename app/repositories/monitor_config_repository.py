from typing import Optional

from app.dtos import MonitorConfig, PathsConfig, SmtpConfig, TimingConfig
from app.services import json_file_service


_monitor_config = None


def load(file_path: str) -> MonitorConfig:
    global _monitor_config
    data = json_file_service.load(file_path)
    _monitor_config = _map(data)
    return _monitor_config


def get() -> MonitorConfig:
    if _monitor_config is None:
        raise RuntimeError("monitor_config_repository.load() must be called first")
    return _monitor_config


def _map(data: dict) -> MonitorConfig:
    smtp_config = SmtpConfig(
        host=data["smtp"]["host"],
        port=data["smtp"]["port"],
        username=data["smtp"]["username"],
        password=data["smtp"]["password"],
        use_tls=data["smtp"]["use_tls"],
        from_address=data["smtp"]["from_address"],
    )
    timing_config = TimingConfig(
        check_interval_in_seconds=data["timing"]["check_interval_in_seconds"],
        check_timeout_in_seconds=data["timing"]["check_timeout_in_seconds"],
        notification_interval_in_seconds=data["timing"]["notification_interval_in_seconds"],
    )
    paths_config = PathsConfig(
        servers_config_file=data["paths"]["servers_config_file"],
        user_info_file=data["paths"]["user_info_file"],
        logs_folder=data["paths"]["logs_folder"],
    )
    return MonitorConfig(smtp=smtp_config, timing=timing_config, paths=paths_config)
