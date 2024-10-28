"""Tests for web about page functionality."""

import pytest
from nicegui.testing import User

from vineapp import __web__
from vineapp.app_info import get_application_info


@pytest.mark.module_under_test(__web__)
async def test_about_page_renders_application_info(user: User) -> None:
    """Test that the about page displays all application information."""
    # Given
    info = get_application_info()
    
    # When
    await user.open("/about")
    
    # Then
    await user.should_see(info.name)
    await user.should_see(info.version)
    await user.should_see(info.description)
    await user.should_see(info.author_email)


@pytest.mark.module_under_test(__web__)
async def test_about_page_contains_required_links(user: User) -> None:
    """Test that the about page contains GitHub and documentation links."""
    # When
    await user.open("/about")
    
    # Then
    await user.should_see("GitHub")
    await user.should_see("Documentation")


@pytest.mark.module_under_test(__web__)
async def test_homepage_links_to_about(user: User) -> None:
    """Test that homepage contains link to about page."""
    # When
    await user.open("/")
    
    # Then
    await user.should_see("About")
    user.find("About").click()
    await user.should_see("About")
