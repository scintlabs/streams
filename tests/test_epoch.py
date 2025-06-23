import pytest
from streams.services.epoch import EpochManager


@pytest.mark.asyncio
async def test_epoch_manager_handle_returns_none(qdrant_client):
    manager = EpochManager()
    msg = {"id": "stub"}
    result = await manager.handle(msg)
    assert result is None
    assert manager.active == {}


def test_epoch_manager_init():
    manager = EpochManager()
    assert manager.active == {}
