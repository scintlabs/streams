from fastapi import APIRouter

from streams.storage import postgres

router = APIRouter(prefix="/api")


@router.get("/providers")
async def list_providers():
    providers = await postgres.get_providers()
    return providers


@router.post("/streams")
async def create_stream(name: str):
    # TODO: insert row + return stream info
    return {"id": "stub", "name": name}
