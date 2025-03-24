import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger

from .defaults import DEFAULT_LOG_FILE, DEFAULT_METADATA, LOG_DIR


def logger_setup(
    level=logging.INFO,
    log_file=DEFAULT_LOG_FILE,
    max_bytes=5 * 1024 * 1024,  # 5MB per file
    backup_count=3,  # Keep last 3 log files
    extra_metadata=None,
    custom_handlers=None,
):
    """
    Configures the root logger with handlers (console, file, or custom).
    Should be called once in the project entry point.
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Ensure 'logs' directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    if not root_logger.hasHandlers():

        # make sure all handlers are using the JsonFormatter
        json_formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(program)s %(hostname)s"
        )

        if custom_handlers:
            for handler in custom_handlers:
                handler.setFormatter(json_formatter)
                root_logger.addHandler(handler)
        else:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(json_formatter)
            root_logger.addHandler(console_handler)

            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setFormatter(json_formatter)
            root_logger.addHandler(file_handler)

    # Include default metadata
    if extra_metadata:
        DEFAULT_METADATA.update(extra_metadata)

    # Attach metadata to all log records
    def log_record_factory(*args, **kwargs):
        record = logging.LogRecord(*args, **kwargs)
        for key, value in DEFAULT_METADATA.items():
            setattr(record, key, value)
        return record

    logging.setLogRecordFactory(log_record_factory)
