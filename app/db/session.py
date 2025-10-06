"""Async database session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.base import Base

async_engine: AsyncEngine = create_async_engine(settings.database_url, echo=False)
SessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a per-request async database session."""

    async with SessionLocal() as session:
        yield session


async def init_database() -> None:
    """Initialise database metadata if needed."""

    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
