import importlib

def test_link_service_import(qdrant_client):
    link = importlib.import_module("streams.services.link")
    assert link is not None
