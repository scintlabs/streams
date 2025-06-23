from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import numpy as np

from streams.config import settings
from streams.services.embeddings import generate
from streams.services.qdrant import client
from qdrant_client import models as qd


class EpochManager:
    def __init__(self):
        # active epochs keyed by stream id
        self.active: dict[str, dict] = {}

    async def handle(self, msg):
        """Process a message and handle epoch boundaries.

        When a barrier is detected (time gap or semantic drift), the current
        epoch is flushed to Qdrant and a new epoch is started. The returned
        Qdrant point id is attached to all messages in that epoch.
        """

        stream_id = msg["stream_id"]
        ts: datetime = msg.get("ts") or datetime.utcnow()
        vector = await generate(msg["content"])

        epoch = self.active.get(stream_id)

        async def _flush(sid: str, data: dict):
            if not data["vectors"]:
                return
            centroid = np.mean(data["vectors"], axis=0).tolist()
            eid = str(uuid4())
            await client.upsert(
                collection_name="epochs",
                points=[
                    qd.PointStruct(
                        id=eid,
                        vector=centroid,
                        payload={"stream": str(sid)},
                    )
                ],
                wait=True,
            )
            for m in data["messages"]:
                m["epoch_id"] = eid

        # determine if we need to close the previous epoch
        barrier = False
        if epoch:
            if epoch.get("last_ts"):
                delta = (ts - epoch["last_ts"]).total_seconds() / 60
                if delta >= settings.TIME_GAP_MINUTES:
                    barrier = True
            if not barrier and epoch["vectors"]:
                centroid = np.mean(epoch["vectors"], axis=0)
                sim = float(
                    np.dot(centroid, vector)
                    / (np.linalg.norm(centroid) * np.linalg.norm(vector))
                )
                if sim < 1 - settings.SEMANTIC_THRESHOLD:
                    barrier = True

        if epoch and barrier:
            await _flush(stream_id, epoch)
            epoch = {"messages": [], "vectors": [], "last_ts": ts}
            self.active[stream_id] = epoch
        elif not epoch:
            epoch = {"messages": [], "vectors": [], "last_ts": ts}
            self.active[stream_id] = epoch

        epoch["messages"].append(msg)
        epoch["vectors"].append(vector)
        epoch["last_ts"] = ts


epoch_manager = EpochManager()
