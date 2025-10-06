"""Product-related API endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.session import get_async_session
from app.schemas import ProductCreate, ProductRead
from app.tasks.price_tracking import schedule_price_check

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductRead])
async def list_products(
    session: AsyncSession = Depends(get_async_session),
) -> list[ProductRead]:
    """List products currently being tracked."""

    products = await crud.get_products(session)
    return list(products)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def register_product(
    payload: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
) -> ProductRead:
    """Register a product for price tracking and schedule the first scrape."""

    product = await crud.create_product(session, payload, commit=False)
    task_id = schedule_price_check(product.id)
    product.tracking_task_id = task_id

    await session.commit()
    await session.refresh(product)

    return product
