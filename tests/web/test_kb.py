"""Tests for knowledge base page functionality."""

import os
from unittest.mock import patch

import pytest
from nicegui import ui
from nicegui.testing import User


@pytest.fixture
def fibery_url():
    """Fixture for Fibery URL."""
    return "https://serra.fibery.io"


@pytest.fixture
def mock_env(fibery_url):
    """Mock environment variables."""
    with patch.dict(os.environ, {"VINEAPP_FIBERY_URL": fibery_url}):
        yield


async def test_kb_page_loads(user: User, mock_env) -> None:
    """Test that the knowledge base page loads and shows expected content."""
    await user.open("/kb")
    await user.should_see("Knowledge Base")
    await user.should_see("Available Databases")


async def test_kb_page_shows_fibery_url(user: User, mock_env, fibery_url) -> None:
    """Test that the knowledge base page shows the Fibery URL as a link."""
    await user.open("/kb")
    await user.should_see(fibery_url)
    await user.should_see(kind=ui.link)


async def test_kb_page_shows_databases(user: User, mock_env) -> None:
    """Test that the knowledge base page shows the list of databases."""
    await user.open("/kb")
    await user.should_see("Available Databases")


async def test_kb_page_requires_env_var(user: User) -> None:
    """Test that the knowledge base page handles missing environment variable."""
    with pytest.raises(ValueError, match="VINEAPP_FIBERY_URL.*not set"):
        await user.open("/kb")
