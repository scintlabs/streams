# Streams

## Local Development

This project uses Postgres and Qdrant. A `docker-compose.yml` file is provided to bring up both services.

```bash
# start the database and vector store
docker compose up -d
```

The Postgres service exposes port `5432` and Qdrant listens on `6333`. Stop the stack with `docker compose down` when finished.
