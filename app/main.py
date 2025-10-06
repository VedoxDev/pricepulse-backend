"""Application entrypoint for the PricePulse backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routes.api import api_router


def create_app() -> FastAPI:
    """Initialise and configure the FastAPI application."""

    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        description="Service for tracking product prices across multiple platforms.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
