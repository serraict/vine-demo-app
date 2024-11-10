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
    space_name = "Public"

    # When
    info = FiberyInfo(base_url=base_url, space_name=space_name)

    # Then
    assert str(info.kb_url) == "https://serra.fibery.io/Public/"
    assert str(info.api_url) == "https://serra.fibery.io/api/graphql/space/Public"
    assert str(info.graphql_url) == "https://serra.fibery.io/api/graphql/space/Public"


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
        "name": "PublicActions",
        "fields": [
            {"name": "id", "type": {"name": "ID"}},
            {"name": "name", "type": {"name": "String"}},
        ],
    }

    # When
    schema = FiberySchema.from_type_info(type_info)

    # Then
    assert schema.name == "PublicActions"
    assert len(schema.fields) == 2
    assert schema.fields[0].name == "id"
    assert schema.fields[0].type_name == "ID"
    assert schema.fields[1].name == "name"
    assert schema.fields[1].type_name == "String"


def test_fibery_schema_validates_type_info():
    """Test that FiberySchema validates type info structure."""
    # Given
    invalid_type_info = {
        "name": "PublicActions",
        # Missing fields key
    }

    # When/Then
    with pytest.raises(ValueError, match="Invalid type info structure"):
        FiberySchema.from_type_info(invalid_type_info)


@patch("vineapp.fibery.graphql.get_fibery_client")
def test_fibery_database_from_name(mock_get_client):
    """Test that FiberyDatabase correctly loads from name."""
    # Given
    schema_response = {
        "data": {
            "__type": {
                "name": "PublicActions",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "publicId", "type": {"name": "String"}},
                    {"name": "creationDate", "type": {"name": "String"}},
                    {"name": "modificationDate", "type": {"name": "String"}},
                    {"name": "rank", "type": {"name": "Float"}},
                    {"name": "createdBy", "type": {"name": "FiberyUser"}},
                    {"name": "description", "type": {"name": "RichField"}},
                    {"name": "name", "type": {"name": "String"}},
                    {"name": "state", "type": {"name": "WorkflowStatePublicActions"}},
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
    db = FiberyDatabase.from_name("actions")

    # Then
    assert db.name == "actions"
    assert db.type_schema.name == "PublicActions"
    assert len(db.type_schema.fields) == 9  # All standard fields
    assert len(db.entities) == 1
    assert db.entities[0].name == "Test Action"
    assert db.entities[0].description == "Test Description"


@patch("vineapp.fibery.graphql.get_fibery_client")
def test_fibery_database_handles_plural_form(mock_get_client):
    """Test that FiberyDatabase handles plural form field names."""
    # Given
    schema_response = {
        "data": {
            "__type": {
                "name": "PublicLearning",
                "fields": [
                    {"name": "id", "type": {"name": "ID"}},
                    {"name": "publicId", "type": {"name": "String"}},
                    {"name": "creationDate", "type": {"name": "String"}},
                    {"name": "modificationDate", "type": {"name": "String"}},
                    {"name": "rank", "type": {"name": "Float"}},
                    {"name": "createdBy", "type": {"name": "FiberyUser"}},
                    {"name": "description", "type": {"name": "RichField"}},
                    {"name": "name", "type": {"name": "String"}},
                    {"name": "state", "type": {"name": "WorkflowStatePublicLearning"}},
                ],
            }
        }
    }

    singular_error = {
        "errors": [
            {
                "message": "Cannot query field 'findLearning' on type 'Query'. Did you mean 'findLearnings'?"
            }
        ]
    }

    plural_response = {
        "data": {
            "findLearnings": [
                {
                    "id": "1",
                    "name": "Test Learning",
                    "description": {"text": "Test Description"},
                }
            ]
        }
    }

    mock_client = Mock()
    mock_client.execute.side_effect = [schema_response, singular_error, plural_response]
    mock_get_client.return_value = mock_client

    # When
    db = FiberyDatabase.from_name("learning")

    # Then
    assert db.name == "learning"
    assert db.type_schema.name == "PublicLearning"
    assert len(db.type_schema.fields) == 9  # All standard fields
    assert len(db.entities) == 1
    assert db.entities[0].name == "Test Learning"
    assert db.entities[0].description == "Test Description"
