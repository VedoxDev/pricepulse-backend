"""Common dependency functions for FastAPI routes."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide the current request-scoped database session."""

    async for session in get_async_session():
        yield session
