"""Configuration management for vineapp."""

import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration."""

    connection_string: str

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Create configuration from environment variables."""
        return cls(
            connection_string=os.getenv(
                "VINEAPP_DB_CONNECTION",
                "sqlite://",  # Default to in-memory SQLite for testing
            )
        )
