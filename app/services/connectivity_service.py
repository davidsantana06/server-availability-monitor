import socket

from app.dtos import ServerConfig
from app.enums import ServerStatus
from app.services import log_service


def check(server_config: ServerConfig, timeout_in_seconds: int) -> ServerStatus:
    try:
        with socket.create_connection(
            (server_config.host, server_config.port),
            timeout=timeout_in_seconds,
        ):
            log_service.emit_debug(
                "%s (%s:%s) is ONLINE",
                server_config.hostname,
                server_config.host,
                server_config.port,
            )
            return ServerStatus.ONLINE
    except (socket.timeout, OSError) as error:
        log_service.emit_debug(
            "%s (%s:%s) is OFFLINE: %s",
            server_config.hostname,
            server_config.host,
            server_config.port,
            error,
        )
        return ServerStatus.OFFLINE
