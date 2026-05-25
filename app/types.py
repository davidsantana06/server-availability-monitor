from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple, Optional, Tuple, TypedDict

if TYPE_CHECKING:
    from .dtos import ServerConfig

from .enums import ServerStatus


DtoValidation = Tuple[bool, Optional[str]]

ServerStatusByHostname = dict[str, ServerStatus]


class StatusDiff(NamedTuple):
    new_offline: list[ServerConfig]
    recovered: list[ServerConfig]
    still_offline: list[ServerConfig]


class CycleResult(NamedTuple):
    statuses: ServerStatusByHostname
    last_notification_at: Optional[datetime]


class RawSmtpConfig(TypedDict):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool
    from_address: str


class RawTimingConfig(TypedDict):
    check_interval_in_seconds: int
    check_timeout_in_seconds: int
    notification_interval_in_seconds: int


class RawPathsConfig(TypedDict):
    servers_config_file: str
    user_info_file: str
    logs_folder: str


class RawMonitorConfig(TypedDict):
    smtp: RawSmtpConfig
    timing: RawTimingConfig
    paths: RawPathsConfig


class RawUserInfo(TypedDict):
    username: str
    email: str


class RawServerConfig(TypedDict):
    hostname: str
    ip: Optional[str]
    dns: Optional[str]
    port: int
