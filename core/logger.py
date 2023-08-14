# core/logger.py

import logging
from config import settings

def get_logger(name):
    """
    Returns a logger with specified name.
    The logger's level and format are set by configuration settings.
    """

    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # Do not add handlers if they are already added
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(settings.LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

