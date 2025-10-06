"""Celery application configuration."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "pricepulse",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_routes={"app.tasks.price_tracking.*": {"queue": "price_tracking"}},
    beat_schedule={
        "scheduled-product-scan": {
            "task": "app.tasks.price_tracking.enqueue_recurring_scrape",
            "schedule": settings.scrape_interval_minutes * 60,
        }
    },
)
