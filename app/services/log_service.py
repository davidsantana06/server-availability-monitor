import logging
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(module)s - %(message)s"


def setup(logs_folder: str) -> None:
    folder = Path(logs_folder)
    folder.mkdir(parents=True, exist_ok=True)

    log_file = folder / (datetime.today().strftime("%Y-%m-%d") + ".log")
    formatter = logging.Formatter(_LOG_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)


def emit_debug(msg: str, *args, **kwargs) -> None:
    logging.debug(msg, *args, stacklevel=2, **kwargs)


def emit_info(msg: str, *args, **kwargs) -> None:
    logging.info(msg, *args, stacklevel=2, **kwargs)


def emit_warning(msg: str, *args, **kwargs) -> None:
    logging.warning(msg, *args, stacklevel=2, **kwargs)


def emit_error(msg: str, *args, **kwargs) -> None:
    logging.error(msg, *args, stacklevel=2, **kwargs)
