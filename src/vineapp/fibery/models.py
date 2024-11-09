"""Fibery data models."""

import os
from pydantic import BaseModel, HttpUrl


class FiberyInfo(BaseModel):
    """Information about Fibery environment."""

    name: str = "Fibery Knowledge Base"
    description: str = "Access Serra Vine's Fibery knowledge base and databases"
    base_url: HttpUrl
    databases: list[str] = []


def get_fibery_info() -> FiberyInfo:
    """Get Fibery environment information from environment variables."""
    base_url = os.getenv("VINEAPP_FIBERY_URL")
    if not base_url:
        raise ValueError("VINEAPP_FIBERY_URL environment variable is not set")

    return FiberyInfo(
        base_url=base_url,
        databases=[
            "Process Segments",
            "Products",
            "Schemas",
        ],
    )
