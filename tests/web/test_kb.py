"""Tests for knowledge base page functionality."""

import os
from unittest.mock import patch, Mock

import pytest
import requests
from nicegui import ui
from nicegui.testing import User

from vineapp.fibery.models import get_fibery_info


@pytest.fixture
def fibery_url():
    """Fixture for Fibery URL."""
    return "https://serra.fibery.io"


@pytest.fixture
def mock_env(fibery_url):
    """Mock environment variables."""
    with patch.dict(
        os.environ,
        {
            "VINEAPP_FIBERY_URL": fibery_url,
            "VINEAPP_FIBERY_SPACE": "Public",
            "VINEAPP_FIBERY_TOKEN": "test-token",
        },
        clear=True,
    ):
        yield


@pytest.fixture
def mock_graphql_response():
    """Mock GraphQL API responses."""
    schema_response = {
        "data": {
            "__type": {
                "name": "PublicActions",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "name", "type": {"name": "String"}},
                    {"name": "description", "type": {"name": "String"}},
                ]
            }
        }
    }
    
    entities_response = {
        "data": {
            "findActions": [
                {
                    "id": "1",
                    "name": "Test Action",
                    "description": "Test Description"
                }
            ]
        }
    }
    
    with patch.object(requests, "post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = [schema_response, entities_response]
        mock_post.return_value = mock_response
        yield


async def test_kb_page_loads(user: User, mock_env) -> None:
    """Test that the knowledge base page loads and shows expected content."""
    # When
    await user.open("/kb")

    # Then
    await user.should_see("Knowledge Base")
    await user.should_see("Available Databases")


async def test_kb_page_shows_fibery_url(user: User, mock_env, fibery_url) -> None:
    """Test that the knowledge base page shows the Fibery URL as a link."""
    # When
    await user.open("/kb")

    # Then
    info = get_fibery_info()
    await user.should_see(str(info.base_url))
    await user.should_see(kind=ui.link)


async def test_kb_page_shows_databases(user: User, mock_env) -> None:
    """Test that the knowledge base page shows the list of databases."""
    # When
    await user.open("/kb")

    # Then
    info = get_fibery_info()
    for db in info.databases:
        await user.should_see(db)


async def test_kb_page_requires_env_var(user: User) -> None:
    """Test that the knowledge base page handles missing environment variable."""
    # When/Then
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="VINEAPP_FIBERY_URL.*not set"):
            await user.open("/kb")


async def test_database_detail_page_loads(user: User, mock_env, mock_graphql_response) -> None:
    """Test that the database detail page loads and shows expected content."""
    # When
    await user.open("/kb/database/actions")

    # Then
    await user.should_see("Actions Database")
    await user.should_see("Schema")
    await user.should_see("Example Entities")


async def test_database_detail_page_shows_schema(user: User, mock_env, mock_graphql_response) -> None:
    """Test that the database detail page shows the schema information."""
    # When
    await user.open("/kb/database/actions")

    # Then
    await user.should_see("Id")  # Field names are capitalized in display
    await user.should_see("Name")
    await user.should_see("Description")
