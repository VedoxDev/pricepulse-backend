"""Pydantic models for product price history entries."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PriceHistoryBase(BaseModel):
    price: Decimal
    checked_at: datetime | None = None


class PriceHistoryCreate(PriceHistoryBase):
    product_id: int


class PriceHistoryRead(PriceHistoryBase):
    id: int
    product_id: int
    checked_at: datetime

    class Config:
        from_attributes = True
