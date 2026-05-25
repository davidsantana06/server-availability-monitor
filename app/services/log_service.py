import logging
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"


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


def get_instance(name: str) -> logging.Logger:
    return logging.getLogger(name)
