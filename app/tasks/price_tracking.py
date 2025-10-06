"""Celery tasks for tracking product prices."""

from __future__ import annotations

from typing import Any

from app.schemas.product import ProductCreate

from .celery_app import celery_app


@celery_app.task(name="app.tasks.price_tracking.track_product_price")
def track_product_price(product_data: dict[str, Any]) -> dict[str, Any]:
    """Placeholder task that will eventually fetch and store the latest price."""

    # TODO: implement actual scraping logic and persistence.
    return {"status": "pending", "product": product_data}


@celery_app.task(name="app.tasks.price_tracking.enqueue_recurring_scrape")
def enqueue_recurring_scrape() -> None:
    """Periodic task executed by Celery beat to schedule scrapes."""

    # TODO: load tracked products and enqueue per-product tasks.
    return None


def schedule_price_check(product: ProductCreate) -> str:
    """Enqueue an immediate price check for a product and return the task id."""

    result = track_product_price.delay(product.model_dump())
    return result.id
