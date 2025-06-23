import asyncpg

from streams.config import settings

_pool = None


async def init_pool(dsn: str):
    global _pool
    _pool = await asyncpg.create_pool(dsn)


async def save_message(stream_id, author, content):
    # Simplified insert; returns dict for demo
    return {
        "id": "stub",
        "stream_id": stream_id,
        "author": author,
        "content": content,
        "epoch_id": None,
    }


async def get_providers():
    """Return a list of providers ordered by creation time."""
    rows = await _pool.fetch(
        "SELECT id, name, created FROM providers ORDER BY created DESC"
    )
    return [dict(r) for r in rows]


async def get_streams():
    """Return a list of streams ordered by creation time."""
    rows = await _pool.fetch(
        "SELECT id, provider_id, name, created FROM streams ORDER BY created DESC"
    )
    return [dict(r) for r in rows]


async def create_provider(name: str):
    """Insert a provider and return the created row."""
    row = await _pool.fetchrow(
        "INSERT INTO providers (name) VALUES ($1) RETURNING id, name, created",
        name,
    )
    return dict(row)


async def create_stream(name: str, provider_id=None):
    """Insert a stream and return the created row."""
    if provider_id is None:
        pid_row = await _pool.fetchrow(
            "SELECT id FROM providers ORDER BY created LIMIT 1"
        )
        if pid_row is None:
            raise RuntimeError("No providers configured")
        provider_id = pid_row["id"]
    row = await _pool.fetchrow(
        "INSERT INTO streams (provider_id, name) VALUES ($1, $2) "
        "RETURNING id, provider_id, name, created",
        provider_id,
        name,
    )
    return dict(row)
