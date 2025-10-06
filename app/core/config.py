"""Application configuration and settings."""

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, FieldValidationInfo, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Ensure values defined in an .env file are available before settings initialisation.
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=False)


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
                    "database_url": "postgresql://postgres:postgres@db:5432/pricepulse",
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

    cors_allow_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Comma-separated origins allowed for CORS.",
    )

    database_url: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/pricepulse",
        description="PostgreSQL connection string.",
    )
    database_echo: bool = Field(default=False, description="Enable SQL echo for debugging.")
    database_pool_size: int = Field(default=5, ge=1, description="Base connection pool size.")
    database_max_overflow: int = Field(default=10, ge=0, description="Maximum overflow connections.")
    database_pool_timeout: int = Field(default=30, ge=1, description="Seconds to wait for a connection.")

    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis connection URI.")

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    scrape_interval_minutes: int = Field(default=60, ge=1, description="Task interval in minutes.")

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def _split_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Allow comma-delimited origins in env vars."""

        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("celery_broker_url", "celery_result_backend", mode="before")
    @classmethod
    def _default_celery_urls(cls, value: str | None, info: FieldValidationInfo) -> str | None:
        """Fallback to the Redis URL when a Celery endpoint is unset."""

        if value:
            return value
        redis_url = info.data.get("redis_url")
        return redis_url

    @property
    def sqlalchemy_async_database_url(self) -> str:
        """Return the SQLAlchemy async database URL, normalising sync URLs when needed."""

        url = str(self.database_url)
        if url.startswith("postgresql+asyncpg://"):
            return url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @property
    def sqlalchemy_sync_database_url(self) -> str:
        """Return sync SQLAlchemy URL using psycopg driver for migrations."""

        url = str(self.database_url)
        if url.startswith("postgresql+psycopg://"):
            return url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    values = Settings()
    return values


settings = get_settings()
