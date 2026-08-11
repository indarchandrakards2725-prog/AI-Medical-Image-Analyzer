from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env."""

    app_name: str = "Chest X-ray Assist"
    app_env: str = "development"
    app_debug: bool = True
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Create the settings object once and reuse it across requests."""
    return Settings()