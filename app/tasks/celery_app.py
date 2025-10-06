"""Celery application configuration bound to Redis."""

from celery import Celery

from app.core.config import settings


BROKER_URL = settings.celery_broker_url or settings.redis_url
RESULT_BACKEND = settings.celery_result_backend or settings.redis_url


def create_celery_app() -> Celery:
    """Initialise Celery using Redis for broker and result backend."""

    app = Celery(
        "pricepulse",
        broker=BROKER_URL,
        backend=RESULT_BACKEND,
        include=["app.tasks.price_tracking"],
    )

    app.conf.task_routes = {"app.tasks.price_tracking.*": {"queue": "price_tracking"}}
    app.conf.update(
        timezone="UTC",
        task_default_queue="default",
        beat_schedule={
            "scheduled-product-scan": {
                "task": "app.tasks.price_tracking.enqueue_recurring_scrape",
                "schedule": settings.scrape_interval_minutes * 60,
            }
        },
    )

    return app


celery_app = create_celery_app()
