"""Logging utilities."""

import logging
from rich.logging import RichHandler


def setup_logger(name: str = "byte_agent", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
