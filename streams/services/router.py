import asyncio
from typing import Set

from fastapi import WebSocket


class StreamRouter:
    def __init__(self, stream_id):
        self.stream_id = stream_id
        self._clients: Set[WebSocket] = set()

    async def broadcast(self, data):
        await asyncio.gather(
            *(
                ws.send_json(data)
                for ws in set(self._clients)
                if ws.client_state.name != "DISCONNECTED"
            )
        )

    def flag_manual_barrier(self):
        pass

    async def disconnect(self, ws: WebSocket):
        self._clients.discard(ws)
