# core/__init__.py

"""
 - The get_logger function creates a new logger with the given name, sets its level from the configuration, and adds a handler that writes log messages to the console.
-  The LOG_FORMAT can be adjusted according to the specific needs of your application.
"""

"""
How to use it ?
from core import get_logger

logger = get_logger(__name__)
logger.info('This is an informational message')


"""

from .logger import get_logger

__all__ = ['get_logger']

