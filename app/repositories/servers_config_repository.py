from typing import Optional

from app.dtos import ServerConfig
from app.services import file_system_service
from app.types import RawServerConfig


_server_configs = []


def load(file_path: str) -> list[ServerConfig]:
    global _server_configs
    data = file_system_service.load_json(file_path)
    _server_configs = [_map_as_dto(item) for item in data]
    return _server_configs


def get_all() -> list[ServerConfig]:
    return _server_configs


def get_by_hostname(hostname: str) -> Optional[ServerConfig]:
    return next((s for s in _server_configs if s.hostname == hostname), None)


def _map_as_dto(raw_server_config: RawServerConfig) -> ServerConfig:
    return ServerConfig(
        hostname=raw_server_config["hostname"],
        host=raw_server_config.get("ip") or raw_server_config.get("dns", ""),
        port=raw_server_config["port"],
    )
