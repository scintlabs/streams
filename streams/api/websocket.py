from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from streams.services.epoch import epoch_manager
from streams.services.router import get_router
from streams.storage import postgres

router = APIRouter()


@router.websocket("/streams/{stream_id}/ws")
async def chat_ws(ws: WebSocket, stream_id: UUID):
    await ws.accept()
    hub = get_router(str(stream_id))
    conn = hub.add_client(ws)
    try:
        async for text in ws.iter_text():
            if not conn.record_inbound():
                # Drop excessive inbound messages
                continue
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
