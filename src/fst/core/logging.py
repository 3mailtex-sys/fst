"""Logging helpers for the application."""

from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure simple, consistent console logging."""

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
