"""Tests for configuration management."""
from vineapp.config import DatabaseConfig


def test_default_connection_string():
    """Test default connection string is SQLite."""
    config = DatabaseConfig.from_env()
    assert config.connection_string == "sqlite://"
    assert config.echo_sql is False


def test_custom_connection_string(monkeypatch):
    """Test custom connection string from environment."""
    test_connection = "dremio://user:pass@localhost:31010/test"
    monkeypatch.setenv("VINEAPP_DB_CONNECTION", test_connection)
    monkeypatch.setenv("VINEAPP_SQL_ECHO", "true")
    
    config = DatabaseConfig.from_env()
    assert config.connection_string == test_connection
    assert config.echo_sql is True
