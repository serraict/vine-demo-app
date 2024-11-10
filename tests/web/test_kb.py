"""Tests for knowledge base page functionality."""

import os
from unittest.mock import patch, Mock

import pytest
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
                    "description": {"text": "Test Description"}
                }
            ]
        }
    }
    
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = [schema_response, entities_response]
        mock_post.return_value = mock_response
        yield


@pytest.fixture
def mock_graphql_schema_error():
    """Mock GraphQL API response with schema error."""
    error_response = {
        "errors": [
            {
                "message": "Type 'PublicActions' not found"
            }
        ]
    }
    
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = error_response
        mock_post.return_value = mock_response
        yield


@pytest.fixture
def mock_graphql_invalid_schema():
    """Mock GraphQL API response with invalid schema structure."""
    invalid_response = {
        "data": {
            "__type": {
                "name": "PublicActions",
                # Missing fields key
            }
        }
    }
    
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = invalid_response
        mock_post.return_value = mock_response
        yield


@pytest.fixture
def mock_graphql_response_plural():
    """Mock GraphQL API responses for plural type names."""
    schema_response = {
        "data": {
            "__type": {
                "name": "PublicLearning",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "name", "type": {"name": "String"}},
                    {"name": "description", "type": {"name": "String"}},
                ]
            }
        }
    }
    
    # First attempt with singular fails
    singular_error = {
        "errors": [
            {
                "message": "Cannot query field 'findLearning' on type 'Query'. Did you mean 'findLearnings'?"
            }
        ]
    }
    
    # Second attempt with plural succeeds
    plural_response = {
        "data": {
            "findLearnings": [
                {
                    "id": "1",
                    "name": "Test Learning",
                    "description": {"text": "Test Description"}
                }
            ]
        }
    }
    
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = [schema_response, singular_error, plural_response]
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
    # Check for schema content in example entity
    await user.should_see("Id")  # Field label in example entity
    await user.should_see("Name")  # Field label in example entity
    await user.should_see("Description")  # Field label in example entity


async def test_database_detail_page_handles_schema_error(
    user: User, mock_env, mock_graphql_schema_error
) -> None:
    """Test that the database detail page handles schema errors."""
    # When
    await user.open("/kb/database/actions")

    # Then
    await user.should_see("Type 'PublicActions' not found")


async def test_database_detail_page_handles_invalid_schema(
    user: User, mock_env, mock_graphql_invalid_schema
) -> None:
    """Test that the database detail page handles invalid schema structure."""
    # When
    await user.open("/kb/database/actions")

    # Then
    await user.should_see("Schema error: Invalid type info structure")


async def test_database_detail_page_handles_plural_types(
    user: User, mock_env, mock_graphql_response_plural
) -> None:
    """Test that the database detail page handles plural type names."""
    # When
    await user.open("/kb/database/learning")

    # Then
    await user.should_see("Learning Database")
    await user.should_see("Test Learning")
    await user.should_see("Test Description")
