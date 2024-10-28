"""Tests for web article pages."""

from nicegui.testing import User


async def test_articles_page_loads(user: User) -> None:
    """Test that the articles page loads and shows expected content."""
    # When
    await user.open("/articles")

    # Then
    await user.should_see("Articles")
    await user.should_see("This page and its subpages are created using an APIRouter")
    await user.should_see("Item 1")
    await user.should_see("Item 2")
    await user.should_see("Item 3")


async def test_articles_page_loads_second_time(user: User) -> None:
    """Test that the articles page loads and shows expected content."""
    # When
    await user.open("/articles")

    # Then
    await user.should_see("Articles")
