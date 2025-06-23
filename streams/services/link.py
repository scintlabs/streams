"""Linking helpers.

This module looks up semantically related messages for newly created chat
messages.  When a new message arrives we embed the content, query Qdrant for the
nearest neighbours and broadcast the results to all connected websocket clients
via :class:`~streams.services.router.StreamRouter`.
"""

from __future__ import annotations



from streams.config import settings
from streams.services.embeddings import generate
from streams.services.qdrant import client
from streams.services.router import StreamRouter


async def emit_links(router: StreamRouter, content: str) -> None:
    """Search Qdrant for messages related to ``content`` and broadcast them.

    Parameters
    ----------
    router:
        Router used to broadcast link frames to active websocket clients.
    content:
        Raw text content of the newly created message.
    """

    # Generate an embedding for the new content and use it to search for the
    # most similar existing messages in Qdrant.
    embedding = await generate(content)

    results = await client.search(
        collection_name="epochs",
        query_vector=embedding,
        with_payload=True,
        limit=settings.TOP_K,
    )

    links: list[dict[str, str]] = []
    for point in results:
        payload = point.payload or {}
        stream_id = payload.get("stream_id")
        if stream_id is not None:
            links.append({"stream": str(stream_id)})

    if links:
        await router.broadcast({"type": "related", "links": links})
