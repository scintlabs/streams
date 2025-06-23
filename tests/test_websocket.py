import uuid
from fastapi.testclient import TestClient
from streams.main import app
from streams.services.epoch import epoch_manager
from streams.storage import postgres


def test_websocket_flow(monkeypatch):
    called = {"saved": False, "handled": False}

    async def fake_save_message(stream_id, author, content):
        called["saved"] = True
        return {
            "id": "stub",
            "stream_id": stream_id,
            "author": author,
            "content": content,
            "epoch_id": None,
        }

    async def fake_handle(msg):
        called["handled"] = True

    monkeypatch.setattr(postgres, "save_message", fake_save_message)
    monkeypatch.setattr(epoch_manager, "handle", fake_handle)

    client = TestClient(app)
    with client.websocket_connect(f"/streams/{uuid.uuid4()}/ws") as ws:
        ws.send_text("hello")

    assert called["saved"]
    assert called["handled"]
