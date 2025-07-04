from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="streams/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    # TODO: query real streams
    return templates.TemplateResponse("index.html", {"request": request})


@router.get(
    "/streams/{stream_id}", response_class=HTMLResponse, include_in_schema=False
)
async def chat(request: Request, stream_id: UUID):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "stream_id": str(stream_id)},
    )
