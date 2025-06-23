import asyncio

from streams.config import settings


async def generate(text: str) -> list[float]:
    # TODO: call your embed API
    await asyncio.sleep(0)  # simulate async call
    return [0.0] * 1536
