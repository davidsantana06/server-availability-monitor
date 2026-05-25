from typing import Optional, Tuple

from app.enums import ServerStatus


DtoValidation = Tuple[bool, Optional[str]]

ServerStatusByHostname = dict[str, ServerStatus]
