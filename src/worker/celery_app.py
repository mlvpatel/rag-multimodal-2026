"""Celery application for background document indexing."""

from celery import Celery

from src.core.config import settings

celery_app = Celery(
    "ultimaterag",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Import tasks so they register with this app. celery_app is already defined
# above, so the circular import (tasks import celery_app) resolves cleanly.
from src.worker import tasks  # noqa: E402,F401
