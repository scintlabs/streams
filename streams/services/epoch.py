from streams.config import settings
from streams.services.embeddings import generate
from streams.services.qdrant import client


class EpochManager:
    def __init__(self):
        self.active = {}

    async def handle(self, msg):
        # TODO: barrier detection & upsert to qdrant
        pass


epoch_manager = EpochManager()
