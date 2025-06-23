import uvicorn
from fastapi import FastAPI

from streams.api.pages import router as pages_router
from streams.api.rest import router as rest_router
from streams.api.websocket import router as ws_router
from streams.services.epoch import epoch_manager

app = FastAPI()
app.include_router(rest_router)
app.include_router(pages_router)
app.include_router(ws_router)


@app.on_event("startup")
async def startup() -> None:
    epoch_manager.start_cleanup_task()


@app.on_event("shutdown")
async def shutdown() -> None:
    epoch_manager.stop_cleanup_task()


if __name__ == "__main__":
    uvicorn.run("streams.main:app", host="0.0.0.0", port=8000, reload=True)
