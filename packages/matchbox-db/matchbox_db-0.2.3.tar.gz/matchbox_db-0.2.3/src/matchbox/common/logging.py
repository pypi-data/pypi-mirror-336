"""Logging utilities."""

import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


logging.basicConfig(
    level=INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)


def get_logger(name: str, custom_format: str = None) -> logging.Logger:
    """Get a logger instance."""
    logger = logging.getLogger(name)

    if custom_format:
        logger.handlers.clear()

        custom_handler = RichHandler(rich_tracebacks=True)
        formatter = logging.Formatter(custom_format)
        custom_handler.setFormatter(formatter)

        logger.addHandler(custom_handler)

        logger.propagate = False

    return logger


logger = get_logger("matchbox")


def get_console():
    """Get the console instance."""
    return Console()


def build_progress_bar(console: Console | None = None) -> Progress:
    """Create a progress bar."""
    if console is None:
        console = get_console()

    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    )
