from typing import Optional

from app.dtos import ServerConfig
from app.services import json_file_service


_server_configs = []


def load(file_path: str) -> list[ServerConfig]:
    global _server_configs
    data = json_file_service.load(file_path)
    _server_configs = [_map(item) for item in data]
    return _server_configs


def get_all() -> list[ServerConfig]:
    return _server_configs


def get_by_hostname(hostname: str) -> Optional[ServerConfig]:
    return next((s for s in _server_configs if s.hostname == hostname), None)


def _map(item: dict) -> ServerConfig:
    return ServerConfig(
        hostname=item["hostname"],
        host=item.get("ip") or item.get("dns", ""),
        port=item["port"],
    )
