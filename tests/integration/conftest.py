"""Pytest fixtures for integration tests."""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from vineapp.products import ProductRepository


@pytest.fixture(scope="session")
def dremio_engine() -> Engine:
    """Create a test database engine."""
    connection_string = os.getenv("VINEAPP_DB_CONNECTION")
    
    if not connection_string:
        pytest.skip("Database connection string not configured")
    
    engine = create_engine(connection_string)
    
    try:
        # Verify connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def product_repository(dremio_engine: Engine) -> ProductRepository:
    """Create a product repository for testing."""
    return ProductRepository(dremio_engine)
