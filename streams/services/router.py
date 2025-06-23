import asyncio
import contextlib
from typing import Set, Optional

from fastapi import WebSocket

from streams.services.epoch import epoch_manager


class StreamRouter:
    def __init__(self, stream_id):
        self.stream_id = stream_id
        self._clients: Set[WebSocket] = set()
        self._hb_task: Optional[asyncio.Task] = None

    async def broadcast(self, data):
        """Send ``data`` to all connected clients.

        Any WebSockets that have already disconnected are pruned before
        sending, and failures during send will result in that client being
        removed from the set as well.
        """

        # drop any clients that are already closed
        for ws in list(self._clients):
            if ws.client_state.name == "DISCONNECTED":
                self._clients.discard(ws)

        tasks = [ws.send_json(data) for ws in self._clients]
        if not tasks:
            return

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for ws, result in zip(list(self._clients), results):
            if isinstance(result, Exception):
                self._clients.discard(ws)

    async def start_heartbeat(self, interval: float = 30.0):
        """Periodically send ``{"type": "ping"}`` frames to keep clients alive."""

        if self._hb_task is not None:
            return

        async def _beat():
            try:
                while True:
                    await asyncio.sleep(interval)
                    await self.broadcast({"type": "ping"})
            except asyncio.CancelledError:
                pass

        self._hb_task = asyncio.create_task(_beat())

    async def stop_heartbeat(self):
        if self._hb_task is not None:
            self._hb_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._hb_task
            self._hb_task = None

    def flag_manual_barrier(self):
        epoch_manager.close_epoch(self.stream_id)

    async def disconnect(self, ws: WebSocket):
        self._clients.discard(ws)
        if not self._clients:
            await self.stop_heartbeat()
