"""Provide log symbols for various log levels."""

import os
import platform
from typing import Dict

from loguru import logger

LOG_DIR = "logs"

logger.remove()

os.makedirs(LOG_DIR, exist_ok=True)

# Logging to the file
logger.add(
    f"{LOG_DIR}/app.log",
    rotation="5 MB",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="INFO",
)

log = logger


class LogManager:

    def __init__(self):
        self.log = log

    def info_log(self, message):
        log.info(message)

    def warn_log(self, message):
        log.warning(message)

    def err_log(self, message):
        log.error(message)


class LogSymbols:
    """Symbols for different statuses"""

    INFO = "ℹ"
    SUCCESS = "✔"
    WARNING = "⚠"
    ERROR = "✖"

    FALLBACKS: Dict[str, str] = {
        "info": "i",
        "success": "v",
        "warning": "!!",
        "error": "x",
    }

    @classmethod
    def get_symbols(cls) -> Dict[str, str]:
        """Determines whether the operating system supports basic characters"""
        return (
            {
                "info": cls.INFO,
                "success": cls.SUCCESS,
                "warning": cls.WARNING,
                "error": cls.ERROR,
            }
            if platform.system() != "Windows"
            else cls.FALLBACKS
        )


# Choose the correct characters depending on the OS
LOG_SYMBOLS = LogSymbols.get_symbols()
