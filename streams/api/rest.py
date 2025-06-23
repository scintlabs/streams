from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/providers")
async def list_providers():
    # TODO: fetch from storage
    return []


@router.post("/streams")
async def create_stream(name: str):
    # TODO: insert row + return stream info
    return {"id": "stub", "name": name}
