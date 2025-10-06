"""Price history endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.session import get_async_session
from app.models import Product
from app.schemas import PriceHistoryRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}/history", response_model=list[PriceHistoryRead])
async def list_price_history(
    product_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[PriceHistoryRead]:
    """Return the stored price history for a product."""

    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    history = await crud.get_price_history(session, product_id)
    return list(history)
