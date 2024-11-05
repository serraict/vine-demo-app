"""Tests for core functionality."""

from vineapp.app_info import ApplicationInfo, get_application_info


def test_get_application_info():
    """Test retrieving application metadata."""
    # When
    info = get_application_info()

    # Then
    assert isinstance(info, ApplicationInfo)
    assert info.name == "vineapp"
    assert info.version  # We don't test exact version as it may change
    assert info.description
    assert info.author_email
    assert info.project_url and info.project_url.startswith("http")
