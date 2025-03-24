import logging

from .defaults import DEFAULT_METADATA


def get_logger(name=None, additional_metadata=None):
    """
    Retrieves a logger (root or named) and attaches additional metadata dynamically.

    - `name`: Logger name (None = root logger).
    - `additional_metadata`: Extra fields added to **this logger only**.
    """
    logger = logging.getLogger(name)

    # If no extra metadata is needed, return the logger directly
    if not additional_metadata:
        return logger

    # Custom log record factory to include both default and custom metadata
    def log_record_factory(*args, **kwargs):
        record = logging.LogRecord(*args, **kwargs)
        for key, value in DEFAULT_METADATA.items():
            setattr(record, key, value)
        for key, value in additional_metadata.items():
            setattr(record, key, value)
        return record

    logging.setLogRecordFactory(log_record_factory)

    return logger
