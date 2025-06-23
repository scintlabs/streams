from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from streams.services.epoch import epoch_manager
from streams.services.router import StreamRouter
from streams.storage import postgres

router = APIRouter()


@router.websocket("/streams/{stream_id}/ws")
async def chat_ws(ws: WebSocket, stream_id: UUID):
    await ws.accept()
    hub = StreamRouter(stream_id)
    try:
        async for text in ws.iter_text():
            if text.strip() == "/new":
                hub.flag_manual_barrier()
                continue
            msg = await postgres.save_message(stream_id, "anon", text)
            await epoch_manager.handle(msg)
            await hub.broadcast({"type": "msg", **msg})
    except WebSocketDisconnect:
        pass
    finally:
        await hub.disconnect(ws)
