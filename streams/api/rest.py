from fastapi import APIRouter

from streams.storage import postgres

router = APIRouter(prefix="/api")


@router.get("/providers")
async def list_providers():
    # TODO: fetch from storage
    return []


@router.post("/streams")
async def create_stream(name: str):
    return await postgres.create_stream(name)
