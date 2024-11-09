"""Tests for Fibery data models."""

import os
from unittest.mock import patch

import pytest
from vineapp.fibery.models import FiberyInfo, get_fibery_info


def test_fibery_info_constructs_urls():
    """Test that FiberyInfo correctly constructs URLs from base URL and space name."""
    # Given
    base_url = "https://serra.fibery.io"
    space_name = "Public"
    info = FiberyInfo(base_url=base_url, space_name=space_name)

    # Then
    assert str(info.kb_url) == "https://serra.fibery.io/Public/"
    assert str(info.api_url) == "https://serra.fibery.io/api/graphql/space/Public"
    assert str(info.graphql_url) == "https://serra.fibery.io/api/graphql/space/Public"


def test_get_fibery_info_requires_base_url():
    """Test that get_fibery_info raises error when base URL is not set."""
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


def test_get_fibery_info_returns_info():
    """Test that get_fibery_info returns FiberyInfo with correct values."""
    # Given
    env = {
        "VINEAPP_FIBERY_URL": "https://serra.fibery.io",
        "VINEAPP_FIBERY_SPACE": "Public",
    }
    with patch.dict(os.environ, env, clear=True):
        # When
        info = get_fibery_info()

        # Then
        assert str(info.base_url).rstrip("/") == env["VINEAPP_FIBERY_URL"]
        assert info.space_name == env["VINEAPP_FIBERY_SPACE"]
        assert isinstance(info.databases, list)
