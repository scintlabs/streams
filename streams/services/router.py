import asyncio
import time
from collections import deque
from typing import Dict

from fastapi import WebSocket


class Connection:
    """Represents a single WebSocket connection."""

    rate_limit = 5  # messages per second
    window = 1.0

    def __init__(self, ws: WebSocket):
        self.ws = ws
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=20)
        self._times: deque[float] = deque()
        self._sender = asyncio.create_task(self._send_loop())

    async def _send_loop(self) -> None:
        while True:
            data = await self.queue.get()
            if data is None:
                break
            try:
                await self.ws.send_json(data)
            except Exception:
                break

    async def send(self, data) -> None:
        try:
            self.queue.put_nowait(data)
        except asyncio.QueueFull:
            # Drop if client cannot keep up
            pass

    def record_inbound(self) -> bool:
        now = time.monotonic()
        self._times.append(now)
        while self._times and now - self._times[0] > self.window:
            self._times.popleft()
        return len(self._times) <= self.rate_limit

    async def close(self) -> None:
        await self.ws.close()
        await self.queue.put(None)
        self._sender.cancel()


class StreamRouter:
    def __init__(self, stream_id):
        self.stream_id = stream_id
        self._clients: Dict[WebSocket, Connection] = {}

    def add_client(self, ws: WebSocket) -> Connection:
        conn = Connection(ws)
        self._clients[ws] = conn
        return conn

    async def broadcast(self, data):
        for ws, conn in list(self._clients.items()):
            if ws.client_state.name == "DISCONNECTED":
                await conn.close()
                self._clients.pop(ws, None)
                continue
            await conn.send(data)

    def flag_manual_barrier(self):
        pass

    async def disconnect(self, ws: WebSocket):
        conn = self._clients.pop(ws, None)
        if conn:
            await conn.close()


_routers: Dict[str, StreamRouter] = {}


def get_router(stream_id: str) -> StreamRouter:
    router = _routers.get(stream_id)
    if not router:
        router = StreamRouter(stream_id)
        _routers[stream_id] = router
    return router
