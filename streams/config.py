from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    POSTGRES_DSN: str = "postgresql://localhost/postgres"
    OPENAI_API_KEY: str = ""

    QDRANT_URL: str = "http://localhost:6333"
    EMBED_MODEL: str = "text-embedding-3-small"
    TIME_GAP_MINUTES: int = 30
    SEMANTIC_THRESHOLD: float = 0.30
    TOP_K: int = 5


settings = Settings()  # import from anywhere
