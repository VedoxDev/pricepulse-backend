"""Celery tasks for tracking product prices."""

from __future__ import annotations

import asyncio
import logging
from decimal import Decimal
from typing import Any

from app import crud
from app.db.session import SessionLocal
from app.models import Product

from .celery_app import celery_app

logger = logging.getLogger(__name__)


async def _track_product_price_async(product_id: int) -> dict[str, Any]:
    """Fetch the latest price for a product and persist it."""

    async with SessionLocal() as session:
        product = await session.get(Product, product_id)
        if product is None:
            logger.warning("Product %s not found when tracking price", product_id)
            return {"status": "not_found", "product_id": product_id}

        # Placeholder pricing logic until scrapers are implemented.
        price = product.last_price or product.target_price or Decimal("0")
        entry = await crud.insert_price(session, product_id, price, commit=True)

    logger.info(
        "Recorded price %.2f for product %s", entry.price, product_id
    )
    return {
        "status": "recorded",
        "product_id": product_id,
        "price": str(entry.price),
        "checked_at": entry.checked_at.isoformat(),
    }


@celery_app.task(name="app.tasks.price_tracking.track_product_price")
def track_product_price(product_id: int) -> dict[str, Any]:
    """Celery task entrypoint for recording the latest product price."""

    try:
        return asyncio.run(_track_product_price_async(product_id))
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Price tracking failed for product %s", product_id)
        raise exc


async def _enqueue_recurring_scrape_async() -> int:
    """Queue price tracking tasks for all active products."""

    async with SessionLocal() as session:
        products = await crud.get_products(session)
        product_ids = [product.id for product in products]

    for product_id in product_ids:
        track_product_price.delay(product_id)

    return len(product_ids)


@celery_app.task(name="app.tasks.price_tracking.enqueue_recurring_scrape")
def enqueue_recurring_scrape() -> dict[str, int]:
    """Periodic task executed by Celery beat to schedule scrapes."""

    try:
        queued = asyncio.run(_enqueue_recurring_scrape_async())
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Failed to enqueue recurring price checks")
        raise exc

    logger.info("Queued %s price tracking tasks", queued)
    return {"queued": queued}


def schedule_price_check(product_id: int) -> str:
    """Enqueue an immediate price check for a product and return the task id."""

    result = track_product_price.delay(product_id=product_id)
    return result.id
