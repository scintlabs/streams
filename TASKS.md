# Streams


## API Layer

- [ ] **`api/rest.py`** – implement `list_providers()` to pull providers from Postgres.
- [ ] **`api/rest.py`** – implement `create_stream(name)` to insert and return a new Stream.
- [ ] **`api/pages.py`** – replace hard-coded demo link in `index()` with real stream list.
- [ ] **`api/websocket.py`** – in `chat_ws()`:
  - [ ] call real `storage.postgres.save_message()`.
  - [ ] invoke `epoch_manager.handle(msg)` and broadcast related links via `services.link`.

## Services

- [ ] **`services/embeddings.py`** – wire up real embedding provider (OpenAI, Ollama, etc.).
- [ ] **`services/epoch.py`** – complete `EpochManager.handle()` barrier logic (time gap, semantic drift, `/new` flag) and Qdrant upserts.
- [ ] **`services/epoch.py`** – (optional) add periodic flush of idle epochs.
- [ ] **`services/link.py`** – implement ANN search in Qdrant and emit `related` frames.
- [ ] **`services/router.py`** – implement `flag_manual_barrier()` to force-close current epoch.
- [ ] **`services/router.py`** – refine `broadcast()` (prune dead sockets / heartbeat).

## Storage / Persistence

- [ ] **`storage/postgres.py`** – finish `init_pool(dsn)` and call from startup.
- [ ] **`storage/postgres.py`** – replace stub in `save_message()` with real `INSERT … RETURNING`.
- [ ] **`storage/postgres.py`** – add helpers: `get_providers()`, `get_streams()`, `create_provider()`, `create_stream()`.
- [ ] **`services/qdrant.py`** – ensure collection creation on app startup with proper payload indexes.

## 4. Templates & Front-End
- [ ] **`templates/index.html`** – render real streams list; add “create stream” UI.
- [ ] **`templates/chat.html`** – add `/new` command UI element; show epoch boundaries; handle WS disconnect gracefully.

## 5. Infrastructure / DevOps
- [ ] Create SQL or Alembic migrations for `providers`, `streams`, `messages`.
 - [x] Add startup lifespan event to call `postgres.init_pool()` and `qdrant.ensure_collection()`.
- [ ] Add `.env` variables (`POSTGRES_DSN`, `OPENAI_API_KEY`) and load via `Settings`.
- [ ] Write unit tests for `EpochManager`, `Linker`, and WebSocket flow.
- [ ] Provide `docker-compose.yml` (Postgres + Qdrant).

## Stretch Goals

- [ ] Anonymous / optional auth mechanism.
- [ ] Message history pagination endpoint.
- [ ] Rate-limit & back-pressure on WebSocket.
- [ ] UI polish: autoscroll, markdown rendering, dark mode.
