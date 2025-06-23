from uuid import UUID

from fastapi import APIRouter, Query

from streams.storage import postgres

router = APIRouter(prefix="/api")


@router.get("/providers")
async def list_providers():
    # TODO: fetch from storage
    return []


@router.post("/streams")
async def create_stream(name: str):
    # TODO: insert row + return stream info
    return {"id": "stub", "name": name}


@router.get("/streams/{stream_id}/messages")
async def list_messages(
    stream_id: UUID, page: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)
):
    offset = page * limit
    messages = await postgres.get_messages(stream_id, offset=offset, limit=limit)
    return messages
