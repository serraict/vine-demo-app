"""Tests for web interface."""

import pytest
from nicegui.testing import User

pytest_plugins = ["nicegui.testing.user_plugin"]


@pytest.mark.asyncio
async def test_homepage_links_to_products(user: User) -> None:
    """Test that homepage contains link to products page."""
    # Import web module to register pages
    from vineapp import __web__  # noqa: F401

    # When
    await user.open("/")

    # Then
    await user.should_see("View Products")
    user.find("View Products").click()
    # Verify we're on the products page by looking for the title
    await user.should_see("Products")
