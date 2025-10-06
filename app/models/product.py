"""SQLAlchemy model representing a tracked product."""

from datetime import datetime

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    """Tracked product with metadata for price monitoring."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    url: Mapped[str] = mapped_column(Text, unique=True)
    platform: Mapped[str] = mapped_column(String(length=50))

    target_price: Mapped[float | None] = mapped_column(nullable=True)
    last_price: Mapped[float | None] = mapped_column(nullable=True)
    currency: Mapped[str | None] = mapped_column(String(length=8), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    tracking_task_id: Mapped[str | None] = mapped_column(String(length=255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
