"""Provide log symbols for various log levels."""

import os
import platform
import sys
from typing import Dict

from loguru import logger
from src.config import config

LOG_DIR = "logs"

logger.remove()

os.makedirs(LOG_DIR, exist_ok=True)


if config.is_debug:
    # Logging to the console
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
        level="DEBUG",
        colorize=True,
    )

# Logging to the file
logger.add(
    f"{LOG_DIR}/app.log",
    rotation="5 MB",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="DEBUG",
)

log = logger


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
