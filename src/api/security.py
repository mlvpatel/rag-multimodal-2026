"""Security utilities: API key auth, rate limiting, input sanitization."""

from typing import Optional

import bleach
from fastapi import Header, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.config import settings

limiter = Limiter(key_func=get_remote_address)


def verify_api_key(
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")
) -> str:
    """Require a matching X-API-Key header on protected endpoints."""
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key


def sanitize_question(text: str) -> str:
    """Strip any HTML or script tags from user input before it is used."""
    return bleach.clean(text, tags=[], strip=True).strip()
