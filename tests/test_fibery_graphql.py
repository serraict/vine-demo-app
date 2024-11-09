"""Tests for Fibery GraphQL client."""

import os
from unittest.mock import patch, Mock

import pytest
import requests
from vineapp.fibery.graphql import FiberyGraphQLClient, get_fibery_client


def test_get_fibery_client_requires_token():
    """Test that get_fibery_client raises error when token is not set."""
    # Given
    with patch.dict(os.environ, {}, clear=True):
        # When/Then
        with pytest.raises(ValueError, match="VINEAPP_FIBERY_TOKEN.*not set"):
            get_fibery_client()


def test_graphql_client_sets_auth_header():
    """Test that GraphQL client sets the authorization header."""
    # Given
    token = "test-token"
    url = "https://test.fibery.io/api/graphql"
    client = FiberyGraphQLClient(url=url, token=token)

    with patch.object(requests, "post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_post.return_value = mock_response

        # When
        client.execute("query { test }")

        # Then
        mock_post.assert_called_once()
        headers = mock_post.call_args[1]["headers"]
        assert headers["Authorization"] == f"Token {token}"
