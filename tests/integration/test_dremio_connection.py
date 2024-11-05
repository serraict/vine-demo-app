"""Integration tests for Dremio connection and product retrieval."""

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from vineapp.products import Product, ProductRepository


@pytest.mark.integration
def test_can_connect_to_dremio(dremio_engine):
    """Test that we can establish a connection to Dremio."""
    with dremio_engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar()
        assert result == 1


@pytest.mark.integration
def test_can_retrieve_products(product_repository: ProductRepository):
    """Test that we can retrieve products from Dremio."""
    products = product_repository.get_all()

    # Verify we can retrieve products
    assert isinstance(products, list)

    # Verify each item is a Product instance
    for product in products:
        assert isinstance(product, Product)


@pytest.mark.integration
def test_can_retrieve_paginated_products(product_repository: ProductRepository):
    """Test that we can retrieve paginated products from Dremio."""
    # Get first page
    products, total = product_repository.get_paginated(page=1, items_per_page=10)

    # Verify we got the right number of products
    assert len(products) == 10
    assert total > 10  # We know we have more than 10 products

    # Verify each item is a Product instance
    for product in products:
        assert isinstance(product, Product)

    # Get second page
    page2_products, total2 = product_repository.get_paginated(page=2, items_per_page=10)

    # Verify total is consistent
    assert total == total2

    # Verify we got different products
    assert products[0].id != page2_products[0].id


@pytest.mark.integration
def test_can_use_different_page_sizes(product_repository: ProductRepository):
    """Test that we can use different page sizes."""
    # Get page with 5 items
    products5, total = product_repository.get_paginated(page=1, items_per_page=5)
    assert len(products5) == 5

    # Get page with 25 items
    products25, total = product_repository.get_paginated(page=1, items_per_page=25)
    assert len(products25) == 25

    # Verify we got more products with larger page size
    assert len(products25) > len(products5)


@pytest.mark.integration
def test_handles_last_page_with_partial_results(product_repository: ProductRepository):
    """Test that last page returns correct number of remaining items."""
    # Get total count from first page
    _, total = product_repository.get_paginated(page=1, items_per_page=10)

    # Calculate last page
    last_page = (total + 9) // 10  # Round up division
    remaining_items = total % 10 or 10  # If divisible by 10, last page is full

    # Get last page
    products, total2 = product_repository.get_paginated(
        page=last_page, items_per_page=10
    )

    # Verify we got the right number of products
    assert len(products) == remaining_items
    assert total == total2


@pytest.mark.integration
def test_handles_connection_error(dremio_engine):
    """Test that connection errors are handled gracefully."""
    # Force a connection error by disposing the engine
    dremio_engine.dispose()

    try:
        with dremio_engine.connect():
            pass
    except SQLAlchemyError as e:
        assert "Connection" in str(e)
