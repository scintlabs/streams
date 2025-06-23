import asyncpg
from uuid import uuid4

from streams.config import settings

_streams: list[dict] = [
    {"id": "00000000-0000-0000-0000-000000000001", "name": "demo-stream"}
]

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


async def get_streams() -> list[dict]:
    """Return available streams."""
    return list(_streams)


async def create_stream(name: str) -> dict:
    """Create a new stream placeholder and return it."""
    stream = {"id": str(uuid4()), "name": name}
    _streams.append(stream)
    return stream
