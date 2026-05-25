from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple, Optional, Tuple

if TYPE_CHECKING:
    from app.dtos import ServerConfig
from app.enums import ServerStatus


DtoValidation = Tuple[bool, Optional[str]]

ServerStatusByHostname = dict[str, ServerStatus]


class StatusDiff(NamedTuple):
    new_offline: list[ServerConfig]
    recovered: list[ServerConfig]
    still_offline: list[ServerConfig]


class CycleResult(NamedTuple):
    statuses: ServerStatusByHostname
    last_notification_at: Optional[datetime]
