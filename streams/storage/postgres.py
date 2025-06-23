"""Postgres connection helpers."""

import logging
from typing import Optional

import asyncpg

from streams.config import settings

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.Pool] = None


async def init_pool(dsn: str) -> asyncpg.Pool:
    """Initialize a shared asyncpg pool.

    The function may be called multiple times; subsequent calls will
    return the previously created pool. Any connection errors are logged
    and re-raised to fail application startup.
    """

    global _pool
    if _pool is not None:
        return _pool
    try:
        _pool = await asyncpg.create_pool(dsn)
    except Exception as exc:  # pragma: no cover - exercised in tests
        logger.error("Failed to create Postgres pool: %s", exc)
        raise
    return _pool


def get_pool() -> asyncpg.Pool:
    """Return the initialized connection pool."""

    if _pool is None:
        raise RuntimeError("Postgres pool has not been initialized")
    return _pool


async def save_message(stream_id, author, content):
    # Simplified insert; returns dict for demo
    return {
        "id": "stub",
        "stream_id": stream_id,
        "author": author,
        "content": content,
        "epoch_id": None,
    }
