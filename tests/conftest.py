"""Test configuration and fixtures."""

from typing import Generator
import pytest
from nicegui.testing import User

pytest_plugins = ["nicegui.testing.user_plugin"]


@pytest.fixture
def user(user: User) -> Generator[User, None, None]:
    """Initialize NiceGUI for testing."""
    from vineapp.web.startup import startup
    startup()
    yield user
