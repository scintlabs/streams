from streams.config import settings
from streams.services.embeddings import generate
from streams.services.qdrant import client


class EpochManager:
    def __init__(self):
        self.active = {}

    def close_epoch(self, stream_id):
        """Force-close the active epoch for ``stream_id``.

        This is used when a client sends the ``/new`` command. By removing the
        current epoch from ``self.active`` we ensure that the next message for
        the stream will start a fresh epoch when ``handle()`` is invoked.
        """

        self.active.pop(stream_id, None)

    async def handle(self, msg):
        # TODO: barrier detection & upsert to qdrant
        pass


epoch_manager = EpochManager()
