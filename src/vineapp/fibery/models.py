"""Fibery data models."""

import os
from typing import Optional
from pydantic import BaseModel, HttpUrl, computed_field


class FiberyInfo(BaseModel):
    """Information about Fibery environment."""

    name: str = "Fibery Knowledge Base"
    description: str = "Access Serra Vine's Fibery knowledge base and databases"
    base_url: HttpUrl
    space_name: str
    databases: list[str] = []

    def _clean_url(self, url: str) -> str:
        """Remove trailing slash from URL."""
        return url.rstrip("/")

    @computed_field(return_type=HttpUrl)
    def kb_url(self) -> HttpUrl:
        """Get the knowledge base URL for this space."""
        base = self._clean_url(str(self.base_url))
        return HttpUrl(f"{base}/{self.space_name}/")

    @computed_field(return_type=HttpUrl)
    def api_url(self) -> HttpUrl:
        """Get the API URL for this space."""
        base = self._clean_url(str(self.base_url))
        return HttpUrl(f"{base}/api/graphql/space/{self.space_name}")

    @computed_field(return_type=HttpUrl)
    def graphql_url(self) -> HttpUrl:
        """Get the GraphQL URL for this space."""
        base = self._clean_url(str(self.base_url))
        return HttpUrl(f"{base}/api/graphql/space/{self.space_name}")


class FiberyEntity(BaseModel):
    """Base model for Fibery entities."""

    id: str
    name: str
    description: Optional[str] = None


def get_fibery_info() -> FiberyInfo:
    """Get Fibery environment information from environment variables."""
    base_url = os.getenv("VINEAPP_FIBERY_URL")
    if not base_url:
        raise ValueError("VINEAPP_FIBERY_URL environment variable is not set")

    space_name = os.getenv("VINEAPP_FIBERY_SPACE")
    if not space_name:
        raise ValueError("VINEAPP_FIBERY_SPACE environment variable is not set")

    return FiberyInfo(
        base_url=base_url.rstrip("/"),
        space_name=space_name,
        databases=[
            "Actions",
            "Learning",
        ],
    )
