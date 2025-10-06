"""Product-related API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.schemas.product import ProductCreate, ProductRead
from app.tasks.price_tracking import schedule_price_check

router = APIRouter()


@router.get("/", response_model=list[ProductRead])
async def list_products(
    session: AsyncSession = Depends(get_async_session),
) -> list[ProductRead]:
    """List products currently being tracked. Placeholder implementation."""

    # TODO: replace with a real database query once models are wired up.
    return []


@router.post("/", response_model=ProductRead, status_code=201)
async def register_product(
    payload: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
) -> ProductRead:
    """Register a product for price tracking and schedule the first scrape."""

    task_id = schedule_price_check(payload)

    # TODO: persist the new product and return it from the database.
    return ProductRead(id=0, tracking_task_id=task_id, **payload.model_dump())
