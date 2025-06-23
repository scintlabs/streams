from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional

from streams.config import settings
from streams.services.embeddings import generate
from streams.services.qdrant import client


class EpochManager:
    """Manage active epochs during a WebSocket session."""

    def __init__(
        self, timeout_seconds: Optional[int] = None, check_interval_seconds: int = 60
    ) -> None:
        # Map epoch_id -> last activity timestamp
        self.active: Dict[str, datetime] = {}
        self.timeout_seconds = timeout_seconds or settings.TIME_GAP_MINUTES * 60
        self.check_interval_seconds = check_interval_seconds
        self._cleanup_task: Optional[asyncio.Task] = None

    async def handle(self, msg):
        # TODO: barrier detection & upsert to qdrant
        pass

    async def _cleanup_loop(self) -> None:
        while True:
            await asyncio.sleep(self.check_interval_seconds)
            cutoff = datetime.utcnow() - timedelta(seconds=self.timeout_seconds)
            for eid, ts in list(self.active.items()):
                if ts < cutoff:
                    self.active.pop(eid, None)

    def start_cleanup_task(self) -> None:
        if not self._cleanup_task or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    def stop_cleanup_task(self) -> None:
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None


epoch_manager = EpochManager()
