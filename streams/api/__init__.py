from .pages import router as pages_router  # ★
from .rest import router as rest_router
from .websocket import router as ws_router

__all__ = ["rest_router", "ws_router", "pages_router"]
