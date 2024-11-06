"""Integration tests for product data access."""

from vineapp.products import Product, ProductRepository
from vineapp.products.models import InvalidParameterError
from sqlalchemy.engine import Engine
from unittest.mock import create_autospec
import pytest


def test_get_all_products(product_repository):
    """Test retrieving all products."""
    products = product_repository.get_all()

    # Verify we get products back
    assert len(products) > 0

    # Verify product structure
    first_product = products[0]
    assert isinstance(first_product, Product)
    assert first_product.id > 0
    # Name and product_group_name could be None in the database
    assert hasattr(first_product, "name")
    assert hasattr(first_product, "product_group_name")
    assert first_product.product_group_id > 0


def test_get_product_by_id(product_repository):
    """Test retrieving a single product by ID."""
    # First get all products to find a valid ID
    products = product_repository.get_all()
    assert len(products) > 0

    # Get a specific product
    product_id = products[0].id
    product = product_repository.get_by_id(product_id)

    # Verify product details
    assert product is not None
    assert product.id == product_id
    assert hasattr(product, "name")  # Name could be None
    assert product.product_group_id > 0
    assert hasattr(product, "product_group_name")  # Group name could be None


def test_get_nonexistent_product(product_repository):
    """Test retrieving a product that doesn't exist."""
    # Try to get a product with an invalid ID
    product = product_repository.get_by_id(-1)
    assert product is None


def test_product_pagination(product_repository):
    """Test product pagination functionality."""
    # Get total count of products
    all_products = product_repository.get_all()
    total_products = len(all_products)

    # Test first page
    products, count = product_repository.get_paginated(page=1, items_per_page=2)
    assert len(products) == min(2, total_products)
    assert count == total_products

    # Test with different page sizes
    products, count = product_repository.get_paginated(page=1, items_per_page=5)
    assert len(products) == min(5, total_products)
    assert count == total_products

    # Test last page
    last_page = (total_products + 4) // 5  # ceiling division
    products, count = product_repository.get_paginated(page=last_page, items_per_page=5)
    assert 0 < len(products) <= 5
    assert count == total_products


def test_product_filtering(product_repository):
    """Test product filtering functionality."""
    # Test with a filter that should return results
    products, count = product_repository.get_paginated(filter_text="T.")
    if count > 0:  # Only check if we found matches
        assert all("T." in p.name for p in products if p.name is not None)

    # Test with a filter that shouldn't return results
    products, count = product_repository.get_paginated(filter_text="NonexistentProduct")
    assert count == 0
    assert len(products) == 0


def test_product_sorting(product_repository):
    """Test product sorting functionality."""

    # Helper function to filter out None values
    def get_non_null_pairs(products, attr):
        return [
            (getattr(products[i], attr), getattr(products[i + 1], attr))
            for i in range(len(products) - 1)
            if getattr(products[i], attr) is not None
            and getattr(products[i + 1], attr) is not None
        ]

    # Test ascending sort by name
    products, _ = product_repository.get_paginated(
        sort_by="name", descending=False, items_per_page=100
    )
    if len(products) > 1:
        # Compare only non-null pairs
        for curr, next_val in get_non_null_pairs(products, "name"):
            assert curr <= next_val

    # Test descending sort by name
    products, _ = product_repository.get_paginated(
        sort_by="name", descending=True, items_per_page=100
    )
    if len(products) > 1:
        # Compare only non-null pairs
        for curr, next_val in get_non_null_pairs(products, "name"):
            assert curr >= next_val


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


def test_pagination_validation():
    """Test pagination parameter validation."""
    repository = ProductRepository(create_autospec(Engine))

    # Test invalid page numbers
    with pytest.raises(
        InvalidParameterError, match="Page number must be greater than 0"
    ):
        repository.get_paginated(page=0)
    with pytest.raises(
        InvalidParameterError, match="Page number must be greater than 0"
    ):
        repository.get_paginated(page=-1)

    # Test invalid items per page
    with pytest.raises(
        InvalidParameterError, match="Items per page must be greater than 0"
    ):
        repository.get_paginated(items_per_page=0)
    with pytest.raises(
        InvalidParameterError, match="Items per page must be greater than 0"
    ):
        repository.get_paginated(items_per_page=-5)
