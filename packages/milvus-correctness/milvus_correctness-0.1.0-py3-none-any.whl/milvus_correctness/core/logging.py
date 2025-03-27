"""Logging configuration for the framework.

This module provides a centralized logging configuration for the entire framework,
using loguru for enhanced logging capabilities.
"""

import sys
from pathlib import Path

from loguru import logger


def get_logger(name: str | None = None) -> logger:
    """Get a logger instance.

    Args:
        name: The name context. If provided, it will be added to the log records.

    Returns:
        The loguru logger instance.
    """
    if name:
        return logger.bind(name=name)
    return logger


def configure_logging(
    log_level: str | int = "INFO",
    log_file: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """Configure logging for the framework.

    Args:
        log_level: The logging level to use. Defaults to INFO.
        log_file: Optional path to log file. If provided, logs will be written to this file.
        max_bytes: Maximum size of each log file in bytes.
        backup_count: Number of backup files to keep.
    """
    # Remove default handler
    logger.remove()

    # Add console handler with custom format
    format_str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    logger.add(
        sys.stdout,
        format=format_str,
        level=log_level,
        colorize=True,
    )

    # Add file handler if log_file is specified
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
            level=log_level,
            rotation=max_bytes,
            retention=backup_count,
            encoding="utf-8",
        )

    # Disable some verbose loggers
    logger.disable("urllib3")
    logger.disable("requests")
