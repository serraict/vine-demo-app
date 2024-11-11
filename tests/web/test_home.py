"""Tests for web homepage functionality."""

from nicegui.testing import User

from .test_kb import mock_env, fibery_url, mock_graphql_response  # noqa: F401


async def test_homepage_loads(user: User) -> None:
    """Test that the homepage loads and shows expected content."""
    # When
    await user.open("/")

    # Then
    await user.should_see("Products")
    await user.should_see("Knowledge Base")
    await user.should_see("About")


async def test_homepage_links_to_products(user: User) -> None:
    """Test that homepage contains link to products page."""
    # When
    await user.open("/")

    # Then
    await user.should_see("View Products")
    user.find("View Products").click()
    await user.should_see("Products")


async def test_homepage_links_to_kb(user: User, mock_env, mock_graphql_response) -> None:  # noqa: F811
    """Test that homepage contains link to knowledge base page."""
    # When
    await user.open("/")

    # Then
    await user.should_see("Knowledge Base")
    user.find("Knowledge Base").click()
    await user.should_see("Available Databases")
