import logging
import socket

from app.dtos import ServerConfig
from app.enums import ServerStatus


logger = logging.getLogger(__name__)


def check(server_config: ServerConfig, timeout_in_seconds: int) -> ServerStatus:
    try:
        with socket.create_connection(
            (server_config.host, server_config.port),
            timeout=timeout_in_seconds,
        ):
            logger.debug(
                "%s (%s:%s) is ONLINE",
                server_config.hostname,
                server_config.host,
                server_config.port,
            )
            return ServerStatus.ONLINE
    except (socket.timeout, OSError) as error:
        logger.debug(
            "%s (%s:%s) is OFFLINE: %s",
            server_config.hostname,
            server_config.host,
            server_config.port,
            error,
        )
        return ServerStatus.OFFLINE
