from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_URL: str = "http://localhost:6333"
    OPENAI_API_KEY: str | None = None
    EMBED_MODEL: str = "text-embedding-3-small"
    TIME_GAP_MINUTES: int = 30
    SEMANTIC_THRESHOLD: float = 0.30
    TOP_K: int = 5


settings = Settings()  # import from anywhere
