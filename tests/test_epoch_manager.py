import asyncio
from datetime import datetime, timedelta

import pytest

from streams.services.epoch import EpochManager


@pytest.mark.asyncio
async def test_cleanup_removes_inactive_epochs():
    manager = EpochManager(timeout_seconds=0.1, check_interval_seconds=0.05)
    # mark an epoch in the past so it should be removed
    manager.active["e1"] = datetime.utcnow() - timedelta(seconds=1)
    manager.start_cleanup_task()
    await asyncio.sleep(0.2)
    manager.stop_cleanup_task()
    assert "e1" not in manager.active
