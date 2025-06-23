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
    if _pool is None:
        raise RuntimeError("Postgres pool not initialized")
    rows = await _pool.fetch("SELECT id, name, created FROM providers ORDER BY created")
    return [dict(r) for r in rows]
