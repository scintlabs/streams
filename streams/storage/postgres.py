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


async def get_streams():
    """Return available streams.

    This placeholder implementation yields a single static entry so that the
    rest of the application can render a stream list without a real database.
    """
    return [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "demo-stream",
        }
    ]
