"""SQLAlchemy models for products and their price history."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    """Tracked product with metadata for price monitoring."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    url: Mapped[str] = mapped_column(Text, unique=True)
    platform: Mapped[str] = mapped_column(String(length=50))

    target_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    last_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(length=8), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    tracking_task_id: Mapped[str | None] = mapped_column(String(length=255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    price_history: Mapped[list["PriceHistory"]] = relationship(
        "PriceHistory",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class PriceHistory(Base):
    """Historical record of product price snapshots."""

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    checked_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product: Mapped[Product] = relationship("Product", back_populates="price_history")
