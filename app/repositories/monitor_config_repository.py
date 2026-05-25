from typing import TypedDict

from app.dtos import MonitorConfig, PathsConfig, SmtpConfig, TimingConfig
from app.services import file_system_service


_RawSmtpConfig = TypedDict(
    "RawSmtpConfig",
    {
        "host": str,
        "port": int,
        "username": str,
        "password": str,
        "use_tls": bool,
        "from_address": str,
    }
)

_RawTimingConfig = TypedDict(
    "RawTimingConfig",
    {
        "check_interval_in_seconds": int,
        "check_timeout_in_seconds": int,
        "notification_interval_in_seconds": int,
    }
)

_RawPathsConfig = TypedDict(
    "RawPathsConfig",
    {
        "servers_config_file": str,
        "user_info_file": str,
        "logs_folder": str,
    }
)

_RawMonitorConfig = TypedDict(
    "RawMonitorConfig",
    {
        "smtp": _RawSmtpConfig,
        "timing": _RawTimingConfig,
        "paths": _RawPathsConfig,
    }
)


_monitor_config = None


def load(file_path: str) -> MonitorConfig:
    global _monitor_config
    raw_monitor_config = file_system_service.load_json(file_path)
    _monitor_config = _map_as_dto(raw_monitor_config)
    return _monitor_config


def get() -> MonitorConfig:
    if _monitor_config is None:
        raise RuntimeError("monitor_config_repository.load() must be called first")
    return _monitor_config


def _map_as_dto(raw_monitor_config: _RawMonitorConfig) -> MonitorConfig:
    return MonitorConfig(
        smtp=SmtpConfig(**raw_monitor_config["smtp"]),
        timing=TimingConfig(**raw_monitor_config["timing"]),
        paths=PathsConfig(**raw_monitor_config["paths"]),
    )
