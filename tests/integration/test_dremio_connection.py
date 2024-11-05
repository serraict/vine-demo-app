"""Integration tests for Dremio connection."""

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from vineapp.products.models import ProductRepository


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
            conn.execute(text("SELECT 1"))
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def product_repository(dremio_engine: Engine) -> ProductRepository:
    """Create a product repository for testing."""
    return ProductRepository(dremio_engine)


def test_can_connect_to_dremio(dremio_engine: Engine) -> None:
    """Test that we can connect to Dremio."""
    with dremio_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_can_get_products(product_repository: ProductRepository) -> None:
    """Test that we can get products from Dremio."""
    products = product_repository.get_all()
    assert len(products) > 0


def test_can_get_product_by_id(product_repository: ProductRepository) -> None:
    """Test that we can get a product by ID."""
    # First get all products to find a valid ID
    products = product_repository.get_all()
    assert len(products) > 0

    # Then get one by ID
    product = product_repository.get_by_id(products[0].id)
    assert product is not None
    assert product.id == products[0].id


def test_can_get_paginated_products(product_repository: ProductRepository) -> None:
    """Test that we can get paginated products."""
    products, total = product_repository.get_paginated(page=1, items_per_page=2)
    assert len(products) == 2
    assert total > 0


def test_can_get_filtered_products(product_repository: ProductRepository) -> None:
    """Test that we can filter products."""
    products, total = product_repository.get_paginated(filter_text="Bee")
    assert len(products) > 0
    assert all("Bee" in p.name for p in products)


def test_default_sorting_order(product_repository: ProductRepository) -> None:
    """Test that default sorting is by product_group_name, then name."""
    products, _ = product_repository.get_paginated(
        page=1,
        items_per_page=100,  # Get enough products to verify sorting
        sort_by=None,  # Use default sorting
    )
    
    # Verify products are ordered by product_group_name, then name
    assert len(products) > 1  # Need at least 2 products to verify ordering
    for i in range(len(products) - 1):
        current = products[i]
        next_product = products[i + 1]
        
        # If product groups are the same, names should be in order
        if current.product_group_name == next_product.product_group_name:
            assert current.name <= next_product.name
        # If product groups are different, they should be in order
        else:
            assert current.product_group_name <= next_product.product_group_name
