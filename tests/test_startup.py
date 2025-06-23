import asyncio

import pytest
from fastapi.testclient import TestClient

from streams.main import app
from streams.storage import postgres
from streams.config import settings


@pytest.mark.asyncio
async def test_startup_calls_init_pool(monkeypatch):
    called = {}
    postgres._pool = None

    async def fake_init_pool(dsn):
        called["dsn"] = dsn

    monkeypatch.setattr(postgres, "init_pool", fake_init_pool)

    # TestClient will trigger startup and shutdown events
    with TestClient(app):
        pass

    assert called["dsn"] == settings.POSTGRES_DSN


@pytest.mark.asyncio
async def test_init_pool_error(monkeypatch):
    async def boom(dsn):
        raise RuntimeError("boom")

    postgres._pool = None
    monkeypatch.setattr(postgres, "asyncpg", type("_m", (), {"create_pool": boom}))
    with pytest.raises(RuntimeError):
        await postgres.init_pool("dsn")
