"""
Custom logger implementation for the Mentat SDK.

This module provides a custom logger that outputs both to a file and to the console,
with colored console output for better readability.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

import coloredlogs


class MentatLogger:
    """
    Custom logger for the Mentat SDK that provides both file and console output.

    The console output is enhanced with colors using the coloredlogs package,
    while file output maintains a detailed log for debugging purposes.
    """

    def __init__(
        self, name: str, log_dir: Optional[str] = None, level: int = logging.INFO
    ) -> None:
        """
        Initialize a new logger instance.

        Args:
            name (str): Name of the logger, used to identify the source of log messages.
            log_dir (Optional[str]): Directory where log files will be stored.
                                   If None, defaults to ~/.mentat/logs
            level (int): The logging level. Defaults to logging.INFO.

        Raises:
            ValueError: If name is empty.
            OSError: If the log directory cannot be created or is not writable.
        """
        if not name:
            raise ValueError("Logger name cannot be empty")

        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Clear any existing handlers
        self.logger.handlers = []

        # Set up log directory
        if log_dir is None:
            log_dir = os.path.expanduser("~/.mentat/logs")

        log_path = Path(log_dir)
        try:
            log_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create log directory at {log_dir}: {e}")

        # Set up file handler
        log_file = log_path / f"mentat_{name}.log"
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Set up console handler with coloredlogs
        coloredlogs.install(
            level=level,
            logger=self.logger,
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout,
        )

    def debug(self, msg: str) -> None:
        """Log a debug message."""
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log an info message."""
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log a warning message."""
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log an error message."""
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """Log a critical message."""
        self.logger.critical(msg)
