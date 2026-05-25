from app.dtos import MonitorConfig, PathsConfig, SmtpConfig, TimingConfig
from app.services import file_system_service
from app.types import RawMonitorConfig


_monitor_config = None


def load(file_path: str) -> MonitorConfig:
    global _monitor_config
    data = file_system_service.load_json(file_path)
    _monitor_config = _map_as_dto(data)
    return _monitor_config


def get() -> MonitorConfig:
    if _monitor_config is None:
        raise RuntimeError("monitor_config_repository.load() must be called first")
    return _monitor_config


def _map_as_dto(raw_monitor_config: RawMonitorConfig) -> MonitorConfig:
    return MonitorConfig(
        smtp=SmtpConfig(**raw_monitor_config["smtp"]),
        timing=TimingConfig(**raw_monitor_config["timing"]),
        paths=PathsConfig(**raw_monitor_config["paths"]),
    )
