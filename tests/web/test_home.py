"""Tests for web homepage functionality."""

from nicegui.testing import User


async def test_homepage_loads(user: User) -> None:
    """Test that the homepage loads and shows expected content."""
    # When
    await user.open("/")

    # Then
    # await user.should_see("Vine App")
    await user.should_see("Products")
    await user.should_see("About")


async def test_homepage_links_to_products(user: User) -> None:
    """Test that homepage contains link to products page."""
    await user.open("/")
    await user.should_see("View Products")
    user.find("View Products").click()
    await user.should_see("Products")
