from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import logging
import sys

from . import file_system_service


_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

_logger = logging.getLogger("SAM")


def setup(logs_folder: str) -> None:
    folder = file_system_service.resolve_path(logs_folder)
    folder.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        filename=str(folder / "sam.log"),
        when="midnight",
        interval=1,
        encoding="utf-8",
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.namer = lambda filename: filename.replace(".log.", ".") + ".log"
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    _logger.setLevel(logging.DEBUG)
    _logger.handlers.clear()
    _logger.propagate = False
    _logger.addHandler(stream_handler)
    _logger.addHandler(file_handler)


def emit_debug(msg: str, *args, **kwargs) -> None:
    _logger.debug(msg, *args, stacklevel=2, **kwargs)


def emit_info(msg: str, *args, **kwargs) -> None:
    _logger.info(msg, *args, stacklevel=2, **kwargs)


def emit_warning(msg: str, *args, **kwargs) -> None:
    _logger.warning(msg, *args, stacklevel=2, **kwargs)


def emit_error(msg: str, *args, **kwargs) -> None:
    _logger.error(msg, *args, stacklevel=2, **kwargs)
