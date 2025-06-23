import os
import pytest
import pytest_asyncio
import asyncpg
from qdrant_client import AsyncQdrantClient
from streams.config import settings


@pytest_asyncio.fixture(scope="session")
async def postgres_pool():
    dsn = os.getenv("POSTGRES_DSN")
    if not dsn:
        pytest.skip("POSTGRES_DSN not set")
    pool = await asyncpg.create_pool(dsn)
    yield pool
    await pool.close()


@pytest_asyncio.fixture(scope="session")
async def qdrant_client():
    try:
        client = AsyncQdrantClient(url=settings.QDRANT_URL)
        await client.get_collections()
    except Exception:
        pytest.skip("Qdrant not available")
    yield client
