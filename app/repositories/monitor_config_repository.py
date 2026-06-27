from typing import TypedDict

from app.dtos import ConcurrencyConfig, MonitorConfig, PathsConfig, SmtpConfig, TimingConfig
from app.services import file_system_service


_RawSmtpConfig = TypedDict(
    "_RawSmtpConfig",
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
    "_RawTimingConfig",
    {
        "check_interval_in_seconds": int,
        "check_timeout_in_seconds": int,
        "notification_interval_in_seconds": int,
    }
)

_RawConcurrencyConfig = TypedDict(
    "_RawConcurrencyConfig",
    {
        "check_workers": int,
    }
)

_RawPathsConfig = TypedDict(
    "_RawPathsConfig",
    {
        "servers_pool_file": str,
        "users_info_file": str,
        "logs_folder": str,
    }
)

_RawMonitorConfig = TypedDict(
    "_RawMonitorConfig",
    {
        "smtp": _RawSmtpConfig,
        "timing": _RawTimingConfig,
        "concurrency": _RawConcurrencyConfig,
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
        concurrency=ConcurrencyConfig(**raw_monitor_config["concurrency"]),
        paths=PathsConfig(**raw_monitor_config["paths"]),
    )
