"""Base interface for product scrapers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.schemas.product import ProductRead


class BaseScraper(ABC):
    """Abstract scraper that fetches price information from a platform."""

    platform: str

    def __init__(self, platform: str) -> None:
        self.platform = platform

    @abstractmethod
    async def fetch_price(self, product: ProductRead) -> dict[str, Any]:
        """Return the latest price information for the given product."""

        raise NotImplementedError
