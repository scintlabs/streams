from openai import AsyncOpenAI

from streams.config import settings


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate(text: str) -> list[float]:
    resp = await client.embeddings.create(
        model=settings.EMBED_MODEL,
        input=text,
    )
    return resp.data[0].embedding
