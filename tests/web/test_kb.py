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
    responses = [
        # Response for schema types query (used by kb page)
        {
            "data": {
                "__schema": {
                    "types": [
                        {
                            "name": "PublicActions",
                            "fields": [
                                {"name": "id", "type": {"name": "ID"}},
                                {"name": "name", "type": {"name": "String"}},
                            ],
                        },
                        {
                            "name": "PublicLearning",
                            "fields": [
                                {"name": "id", "type": {"name": "ID"}},
                                {"name": "name", "type": {"name": "String"}},
                            ],
                        },
                    ]
                }
            }
        },
        # Response for type schema query (used by database page)
        {
            "data": {
                "__type": {
                    "name": "PublicActions",
                    "fields": [
                        {"name": "id", "type": {"name": "ID"}},
                        {"name": "name", "type": {"name": "String"}},
                        {"name": "description", "type": {"name": "String"}},
                    ],
                }
            }
        },
        # Response for entities query (used by database page)
        {
            "data": {
                "findActions": [
                    {
                        "id": "1",
                        "name": "Test Action",
                        "description": {"text": "Test Description"},
                    }
                ]
            }
        },
    ]

    with patch("requests.post") as mock_post:

        def mock_post_side_effect(*args, **kwargs):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            # Get the current query being made
            query = kwargs.get("json", {}).get("query", "")
            print(f"\nReceived query: {query}")

            if "__schema" in query:
                print("Returning schema types response")
                mock_response.json.return_value = responses[0]
            elif "__type" in query:
                print("Returning type schema response")
                mock_response.json.return_value = responses[1]
            else:
                print("Returning entities response")
                mock_response.json.return_value = responses[2]

            return mock_response

        mock_post.side_effect = mock_post_side_effect
        yield


@pytest.fixture
def mock_graphql_schema_error():
    """Mock GraphQL API response with schema error."""
    error_response = {"errors": [{"message": "Type 'PublicActions' not found"}]}

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
    responses = [
        # Response for schema types query
        {
            "data": {
                "__schema": {
                    "types": [
                        {
                            "name": "PublicLearning",
                            "fields": [
                                {"name": "id", "type": {"name": "ID"}},
                                {"name": "name", "type": {"name": "String"}},
                            ],
                        }
                    ]
                }
            }
        },
        # Response for type schema query
        {
            "data": {
                "__type": {
                    "name": "PublicLearning",
                    "fields": [
                        {"name": "id", "type": {"name": "ID"}},
                        {"name": "name", "type": {"name": "String"}},
                        {"name": "description", "type": {"name": "String"}},
                    ],
                }
            }
        },
        # Response for singular entities query (fails)
        {
            "errors": [
                {
                    "message": "Cannot query field 'findLearning' on type 'Query'. Did you mean 'findLearnings'?"
                }
            ]
        },
        # Response for plural entities query (succeeds)
        {
            "data": {
                "findLearnings": [
                    {
                        "id": "1",
                        "name": "Test Learning",
                        "description": {"text": "Test Description"},
                    }
                ]
            }
        },
    ]

    with patch("requests.post") as mock_post:

        def mock_post_side_effect(*args, **kwargs):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            # Get the current query being made
            query = kwargs.get("json", {}).get("query", "")
            print(f"\nReceived query: {query}")

            if "__schema" in query:
                print("Returning schema types response")
                mock_response.json.return_value = responses[0]
            elif "__type" in query:
                print("Returning type schema response")
                mock_response.json.return_value = responses[1]
            elif (
                "findLearning " in query
            ):  # Note the space to avoid matching findLearnings
                print("Returning singular error response")
                mock_response.json.return_value = responses[2]
            else:
                print("Returning plural response")
                mock_response.json.return_value = responses[3]

            return mock_response

        mock_post.side_effect = mock_post_side_effect
        yield


async def test_kb_page_loads(user: User, mock_env, mock_graphql_response) -> None:
    """Test that the knowledge base page loads and shows expected content."""
    # When
    await user.open("/kb")

    # Then
    await user.should_see("Knowledge Base")
    await user.should_see("Available Databases")


async def test_kb_page_shows_fibery_url(
    user: User, mock_env, mock_graphql_response
) -> None:
    """Test that the knowledge base page shows the Fibery URL as a link."""
    # When
    await user.open("/kb")

    # Then
    info = get_fibery_info()
    await user.should_see(str(info.base_url))
    await user.should_see(kind=ui.link)


async def test_kb_page_shows_databases(
    user: User, mock_env, mock_graphql_response
) -> None:
    """Test that the knowledge base page shows the list of databases."""
    # When
    await user.open("/kb")

    # Then
    await user.should_see("Actions")
    await user.should_see("Learning")


async def test_kb_page_requires_env_var(user: User) -> None:
    """Test that the knowledge base page handles missing environment variable."""
    # When/Then
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="VINEAPP_FIBERY_URL.*not set"):
            await user.open("/kb")


async def test_database_detail_page_loads(
    user: User, mock_env, mock_graphql_response
) -> None:
    """Test that the database detail page loads and shows expected content."""
    # When
    await user.open("/kb/database/Actions")

    # Then
    await user.should_see("Actions Database")
    await user.should_see("Schema")
    await user.should_see("Example Entities")


async def test_database_detail_page_shows_schema(
    user: User, mock_env, mock_graphql_response
) -> None:
    """Test that the database detail page shows the schema information."""
    # When
    await user.open("/kb/database/Actions")

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
    await user.open("/kb/database/Actions")

    # Then
    await user.should_see("Type 'PublicActions' not found")


async def test_database_detail_page_handles_invalid_schema(
    user: User, mock_env, mock_graphql_invalid_schema
) -> None:
    """Test that the database detail page handles invalid schema structure."""
    # When
    await user.open("/kb/database/Actions")

    # Then
    await user.should_see("Schema error: Invalid type info structure")


async def test_database_detail_page_handles_plural_types(
    user: User, mock_env, mock_graphql_response_plural
) -> None:
    """Test that the database detail page handles plural type names."""
    # When
    await user.open("/kb/database/Learning")

    # Then
    await user.should_see("Learning Database")
    await user.should_see("Test Learning")
    await user.should_see("Test Description")
