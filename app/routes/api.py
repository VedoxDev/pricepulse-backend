"""Root API router."""

from fastapi import APIRouter

from . import products

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])


@api_router.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Return a simple health status payload."""

    return {"status": "ok"}
