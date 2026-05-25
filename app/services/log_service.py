import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
_LOG_FILE_NAME = "monitor.log"


def setup(logs_folder: str) -> None:
    folder = Path(logs_folder)
    folder.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        filename=folder / _LOG_FILE_NAME,
        when="H",
        interval=24,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
