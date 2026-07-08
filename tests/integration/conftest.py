"""Shared fixtures for integration tests that require the live data stack."""

import psycopg
import pytest

from src.core.config import settings


@pytest.fixture(scope="session")
def pg_available():
    """Skip the whole integration test if Postgres is not reachable."""
    try:
        with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
    except Exception as exc:
        pytest.skip(f"Postgres not reachable at {settings.database_url}: {exc}")
    return True
