"""Helpers for emitting related conversation links."""

from __future__ import annotations

from streams.services.router import StreamRouter


async def emit_related(hub: StreamRouter, msg: dict) -> None:
    """Broadcast placeholder "related" frame to connected clients.

    This will eventually query Qdrant for semantic neighbours of ``msg`` and
    include links to those conversations.  For now it simply sends an empty
    payload so the front-end can react to the event type.
    """

    await hub.broadcast({"type": "related", "links": []})

