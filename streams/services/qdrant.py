from qdrant_client import AsyncQdrantClient
from qdrant_client import models as qd

from streams.config import settings

client = AsyncQdrantClient(url=settings.QDRANT_URL)


async def ensure_collection():
    await client.create_collection(
        collection_name="epochs",
        vectors_config=qd.VectorParams(size=1536, distance="Cosine"),
    )
