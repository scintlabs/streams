import asyncpg

from streams.config import settings

_pool = None


async def init_pool(dsn: str):
    global _pool
    _pool = await asyncpg.create_pool(dsn)


async def save_message(stream_id, author, content):
    query = (
        "INSERT INTO messages (stream_id, author, content) "
        "VALUES ($1, $2, $3) "
        "RETURNING id, stream_id, author, content, ts, epoch_id"
    )
    row = await _pool.fetchrow(query, stream_id, author, content)
    return dict(row)
