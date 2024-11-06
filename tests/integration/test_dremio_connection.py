"""Integration tests for Dremio connection.

This module provides and Engine fixture for connecting to Dremio.

Pytest fixtures use dependency injection by name.
See the doc strings for examples.
"""

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from vineapp.products.models import ProductRepository


@pytest.fixture(scope="session")
def dremio_engine() -> Engine:
    """Create a test database engine.

    This fixture provides a SQLAlchemy Engine instance for connecting to Dremio.
    It's session-scoped for efficiency and ensures proper cleanup.

    Example:
        def test_execute_query(dremio_engine: Engine):
            with dremio_engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM products"))
                assert result.rowcount > 0
    """
    connection_string = os.getenv("VINEAPP_DB_CONNECTION")

    if not connection_string:
        pytest.skip("Database connection string not configured")

    engine = create_engine(connection_string)

    try:
        # Verify connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def product_repository(dremio_engine: Engine) -> ProductRepository:
    """Create a product repository for testing.

    This fixture provides a ProductRepository instance configured with the test database engine.

    Example:
        def test_get_products(product_repository: ProductRepository):
            products = product_repository.get_all()
            assert len(products) > 0
    """
    return ProductRepository(dremio_engine)


def test_can_connect_to_dremio(dremio_engine: Engine) -> None:
    """Test that we can connect to Dremio."""
    with dremio_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
