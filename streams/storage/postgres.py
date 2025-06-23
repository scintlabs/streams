import asyncpg
from collections import defaultdict
from uuid import uuid4

from streams.config import settings

_pool = None
_messages_by_stream = defaultdict(list)


async def init_pool(dsn: str):
    global _pool
    _pool = await asyncpg.create_pool(dsn)


async def save_message(stream_id, author, content):
    msg = {
        "id": str(uuid4()),
        "stream_id": str(stream_id),
        "author": author,
        "content": content,
        "epoch_id": None,
    }
    _messages_by_stream[str(stream_id)].append(msg)
    return msg


async def get_messages(stream_id, offset: int = 0, limit: int = 20):
    msgs = _messages_by_stream.get(str(stream_id), [])
    return msgs[offset : offset + limit]
