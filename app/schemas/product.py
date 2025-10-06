"""Pydantic models for the product domain."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl, field_validator

from app.schemas.price_history import PriceHistoryRead


class ProductBase(BaseModel):
    name: str | None = None
    url: HttpUrl
    platform: str
    target_price: Decimal | None = None
    currency: str | None = None

    @field_validator("platform")
    @classmethod
    def normalise_platform(cls, value: str) -> str:
        """Normalise platform names for consistency."""

        return value.lower()


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    is_active: bool | None = None
    last_price: Decimal | None = None


class ProductRead(ProductBase):
    id: int
    tracking_task_id: str | None = None
    is_active: bool = True
    last_price: Decimal | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    price_history: list[PriceHistoryRead] | None = None

    class Config:
        from_attributes = True
