"""Tests for web about page functionality."""

from nicegui.testing import User

from vineapp.app_info import get_application_info


async def test_about_page_shows_app_info(user: User) -> None:
    """Test that the about page shows application information."""
    # Given
    info = get_application_info()

    # When
    await user.open("/about")

    # Then
    await user.should_see(info.name)
    await user.should_see(info.version)
    await user.should_see(info.description)
    await user.should_see(info.author_email)
    await user.should_see("Project Url")
