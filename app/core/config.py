"""Application configuration and settings."""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings loaded from environment variables or an optional .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        json_schema_extra={
            "examples": [
                {
                    "project_name": "PricePulse",
                    "database_url": "postgresql+asyncpg://postgres:postgres@db:5432/pricepulse",
                    "redis_url": "redis://redis:6379/0",
                }
            ]
        },
    )

    project_name: str = "PricePulse"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/pricepulse",
        description="SQLAlchemy database URL.",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis connection URI.")

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    scrape_interval_minutes: int = Field(default=60, ge=1, description="Task interval in minutes.")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    values = Settings()

    if not values.celery_broker_url:
        values.celery_broker_url = values.redis_url
    if not values.celery_result_backend:
        values.celery_result_backend = values.redis_url

    return values


settings = get_settings()
