"""Application logging setup."""

import logging
import sys

from src.core.config import settings

logger = logging.getLogger("ultimaterag")


def configure_logging() -> None:
    """Configure root logging once, to stdout, at the configured level."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


configure_logging()
