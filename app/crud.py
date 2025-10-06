"""Data access helpers for products and price history."""

from __future__ import annotations

from decimal import Decimal
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import PriceHistory, Product
from app.schemas import ProductCreate


def _to_decimal(value: Decimal | float | int | str) -> Decimal:
    """Normalise incoming numeric values to Decimal."""

    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


async def create_product(
    session: AsyncSession,
    data: ProductCreate,
    *,
    commit: bool = True,
) -> Product:
    """Persist a new product and return the ORM instance."""

    product = Product(
        name=data.name,
        url=str(data.url),
        platform=data.platform,
        target_price=data.target_price,
        currency=data.currency,
    )
    session.add(product)

    if commit:
        await session.commit()
        await session.refresh(product)
    else:
        await session.flush()

    return product


async def get_products(session: AsyncSession) -> Sequence[Product]:
    """Return all tracked products ordered by creation date."""

    statement = select(Product).options(selectinload(Product.price_history)).order_by(Product.created_at.desc())
    result = await session.execute(statement)
    return result.scalars().unique().all()


async def get_price_history(session: AsyncSession, product_id: int) -> Sequence[PriceHistory]:
    """Return stored price snapshots for the given product."""

    statement = (
        select(PriceHistory)
        .where(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.checked_at.desc())
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def insert_price(
    session: AsyncSession,
    product_id: int,
    price: Decimal | float | int | str,
    *,
    commit: bool = True,
) -> PriceHistory:
    """Insert a new price history entry and update the product's last price."""

    product = await session.get(Product, product_id)
    if product is None:
        raise ValueError(f"Product {product_id} not found")

    price_value = _to_decimal(price)
    entry = PriceHistory(product_id=product_id, price=price_value)
    session.add(entry)
    product.last_price = price_value

    if commit:
        await session.commit()
        await session.refresh(entry)
        await session.refresh(product)
    else:
        await session.flush()

    return entry
