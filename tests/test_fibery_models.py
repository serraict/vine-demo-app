"""Tests for Fibery models."""

import os
from unittest.mock import patch, Mock

import pytest

from vineapp.fibery.models import (
    FiberyEntity,
    FiberyField,
    FiberyInfo,
    FiberySchema,
    FiberyDatabase,
    get_fibery_info,
)


def test_fibery_entity_constructs():
    """Test that FiberyEntity correctly constructs from valid data."""
    # Given
    data = {
        "id": "123",
        "name": "Test Entity",
        "description": "Test Description",
    }

    # When
    entity = FiberyEntity(**data)

    # Then
    assert entity.id == "123"
    assert entity.name == "Test Entity"
    assert entity.description == "Test Description"


def test_fibery_info_constructs_urls():
    """Test that FiberyInfo correctly constructs URLs from base URL and space name."""
    # Given
    base_url = "https://serra.fibery.io"
    space_name = "TestSpace"

    # When
    info = FiberyInfo(base_url=base_url, space_name=space_name)

    # Then
    assert str(info.kb_url) == "https://serra.fibery.io/TestSpace/"
    assert str(info.api_url) == "https://serra.fibery.io/api/graphql/space/TestSpace"
    assert (
        str(info.graphql_url) == "https://serra.fibery.io/api/graphql/space/TestSpace"
    )


def test_fibery_info_handles_spaces_in_space_name():
    """Test that FiberyInfo correctly handles spaces in space names."""
    # Given
    base_url = "https://serra.fibery.io"
    space_name = "Test Space Name"

    # When
    info = FiberyInfo(base_url=base_url, space_name=space_name)

    # Then
    assert str(info.kb_url) == "https://serra.fibery.io/Test_Space_Name/"
    assert (
        str(info.api_url) == "https://serra.fibery.io/api/graphql/space/Test_Space_Name"
    )
    assert (
        str(info.graphql_url)
        == "https://serra.fibery.io/api/graphql/space/Test_Space_Name"
    )


def test_get_fibery_info_requires_url():
    """Test that get_fibery_info raises error when URL is not set."""
    # Given
    with patch.dict(os.environ, {}, clear=True):
        # When/Then
        with pytest.raises(ValueError, match="VINEAPP_FIBERY_URL.*not set"):
            get_fibery_info()


def test_get_fibery_info_requires_space_name():
    """Test that get_fibery_info raises error when space name is not set."""
    # Given
    with patch.dict(
        os.environ, {"VINEAPP_FIBERY_URL": "https://serra.fibery.io"}, clear=True
    ):
        # When/Then
        with pytest.raises(ValueError, match="VINEAPP_FIBERY_SPACE.*not set"):
            get_fibery_info()


def test_get_fibery_info_allows_space_override():
    """Test that get_fibery_info allows overriding the space name."""
    # Given
    with patch.dict(
        os.environ,
        {
            "VINEAPP_FIBERY_URL": "https://serra.fibery.io",
            "VINEAPP_FIBERY_SPACE": "Original Space",
        },
        clear=True,
    ):
        # When
        info = get_fibery_info(space_name="ICT Wetering Potlilium")

        # Then
        assert info.space_name == "ICT Wetering Potlilium"
        assert str(info.kb_url) == "https://serra.fibery.io/ICT_Wetering_Potlilium/"


def test_fibery_field_extracts_type_name():
    """Test that FiberyField correctly extracts type name from GraphQL type object."""
    # Given
    data = {
        "name": "test_field",
        "type": {"name": "String"},
    }

    # When
    field = FiberyField(**data)

    # Then
    assert field.name == "test_field"
    assert field.type_name == "String"


def test_fibery_field_handles_missing_type_name():
    """Test that FiberyField handles missing type name gracefully."""
    # Given
    data = {
        "name": "test_field",
        "type": {},  # Missing name key
    }

    # When
    field = FiberyField(**data)

    # Then
    assert field.name == "test_field"
    assert field.type_name == "Unknown"


def test_fibery_schema_from_type_info():
    """Test that FiberySchema correctly constructs from GraphQL type info."""
    # Given
    type_info = {
        "name": "TestSpaceActions",
        "fields": [
            {"name": "id", "type": {"name": "ID"}},
            {"name": "name", "type": {"name": "String"}},
        ],
    }

    # When
    schema = FiberySchema.from_type_info(type_info)

    # Then
    assert schema.name == "TestSpaceActions"
    assert len(schema.fields) == 2
    assert schema.fields[0].name == "id"
    assert schema.fields[0].type_name == "ID"
    assert schema.fields[1].name == "name"
    assert schema.fields[1].type_name == "String"


def test_fibery_schema_validates_type_info():
    """Test that FiberySchema validates type info structure."""
    # Given
    invalid_type_info = {
        "name": "TestSpaceActions",
        # Missing fields key
    }

    # When/Then
    with pytest.raises(ValueError, match="Invalid type info structure"):
        FiberySchema.from_type_info(invalid_type_info)


@patch("vineapp.fibery.graphql.get_fibery_client")
def test_fibery_database_from_name(mock_get_client):
    """Test that FiberyDatabase correctly loads from name."""
    # Given
    space_name = "TestSpace"
    schema_response = {
        "data": {
            "__type": {
                "name": "TestSpaceAction",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "publicId", "type": {"name": "String"}},
                    {"name": "creationDate", "type": {"name": "String"}},
                    {"name": "modificationDate", "type": {"name": "String"}},
                    {"name": "rank", "type": {"name": "Float"}},
                    {"name": "createdBy", "type": {"name": "FiberyUser"}},
                    {"name": "description", "type": {"name": "RichField"}},
                    {"name": "name", "type": {"name": "String"}},
                    {"name": "state", "type": {"name": "WorkflowStateTestSpaceAction"}},
                ],
            }
        }
    }

    entities_response = {
        "data": {
            "findActions": [
                {
                    "id": "1",
                    "name": "Test Action",
                    "description": {"text": "Test Description"},
                }
            ]
        }
    }

    mock_client = Mock()
    mock_client.execute.side_effect = [schema_response, entities_response]
    mock_get_client.return_value = mock_client

    # When
    db = FiberyDatabase.from_name("action", space_name)

    # Then
    assert db.name == "action"
    assert db.type_schema.name == "TestSpaceAction"
    assert len(db.type_schema.fields) == 9  # All standard fields
    assert len(db.entities) == 1
    assert db.entities[0].name == "Test Action"
    assert db.entities[0].description == "Test Description"


@patch("vineapp.fibery.graphql.get_fibery_client")
def test_fibery_database_handles_type_ending_with_s(mock_get_client):
    """Test that FiberyDatabase correctly handles type names ending with 's'."""
    # Given
    space_name = "TestSpace"
    schema_response = {
        "data": {
            "__type": {
                "name": "TestSpaceNews",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "publicId", "type": {"name": "String"}},
                    {"name": "creationDate", "type": {"name": "String"}},
                    {"name": "modificationDate", "type": {"name": "String"}},
                    {"name": "rank", "type": {"name": "Float"}},
                    {"name": "createdBy", "type": {"name": "FiberyUser"}},
                    {"name": "description", "type": {"name": "RichField"}},
                    {"name": "name", "type": {"name": "String"}},
                    {"name": "state", "type": {"name": "WorkflowStateTestSpaceNews"}},
                ],
            }
        }
    }

    entities_response = {
        "data": {
            "findNews": [
                {
                    "id": "1",
                    "name": "Test News",
                    "description": {"text": "Test Description"},
                }
            ]
        }
    }

    mock_client = Mock()
    mock_client.execute.side_effect = [schema_response, entities_response]
    mock_get_client.return_value = mock_client

    # When
    db = FiberyDatabase.from_name("news", space_name)

    # Then
    assert db.name == "news"
    assert db.type_schema.name == "TestSpaceNews"
    assert len(db.type_schema.fields) == 9  # All standard fields
    assert len(db.entities) == 1
    assert db.entities[0].name == "Test News"
    assert db.entities[0].description == "Test Description"


@patch("vineapp.fibery.graphql.get_fibery_client")
def test_fibery_database_handles_spaces_in_space_name(mock_get_client):
    """Test that FiberyDatabase correctly handles spaces in space names."""
    # Given
    space_name = "Test Space Name"
    schema_response = {
        "data": {
            "__type": {
                "name": "TestSpaceNameAction",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "name", "type": {"name": "String"}},
                ],
            }
        }
    }

    entities_response = {
        "data": {
            "findActions": [
                {
                    "id": "1",
                    "name": "Test Action",
                    "description": {"text": "Test Description"},
                }
            ]
        }
    }

    mock_client = Mock()
    mock_client.execute.side_effect = [schema_response, entities_response]
    mock_get_client.return_value = mock_client

    # When
    db = FiberyDatabase.from_name("action", space_name)

    # Then
    assert db.name == "action"
    assert db.type_schema.name == "TestSpaceNameAction"  # No spaces in type name
    assert len(db.entities) == 1
    assert db.entities[0].name == "Test Action"
