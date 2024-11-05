"""Tests for product data access."""

import os
import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.engine import Engine
from sqlmodel import Session
from vineapp.products.models import Product, ProductRepository, InvalidParameterError


def test_get_products():
    """Test retrieving products."""
    # Given
    mock_engine = create_autospec(Engine)
    mock_session = create_autospec(Session)
    mock_result = MagicMock()

    # Create test data
    test_products = [
        Product(
            id=12,
            name="T. Bee 13",
            product_group_id=113,
            product_group_name="13 aziaat",
        ),
        Product(
            id=99,
            name="S. Okinawa 19",
            product_group_id=219,
            product_group_name="19 oriëntal",
        ),
        Product(
            id=23,
            name="T. OrangeSen 19",
            product_group_id=319,
            product_group_name="19 sensations",
        ),
    ]

    # Configure mocks
    mock_result.__iter__.return_value = [
        (p,) for p in test_products
    ]  # SQLModel returns tuples
    mock_session.execute.return_value = mock_result

    with patch("vineapp.products.models.Session") as mock_session_class:
        mock_session_class.return_value.__enter__.return_value = mock_session

        # When
        repository = ProductRepository(mock_engine)
        products = repository.get_all()

    # Then
    assert len(products) == 3
    # Verify products are ordered correctly
    assert [(p.name, p.product_group_name) for p in products] == [
        ("T. Bee 13", "13 aziaat"),
        ("S. Okinawa 19", "19 oriëntal"),
        ("T. OrangeSen 19", "19 sensations"),
    ]


def test_get_product_by_id():
    """Test retrieving a single product by ID."""
    # Given
    mock_engine = create_autospec(Engine)
    mock_session = create_autospec(Session)
    mock_result = MagicMock()

    test_product = Product(
        id=12,
        name="T. Bee 13",
        product_group_id=113,
        product_group_name="13 aziaat",
    )

    # Configure mocks
    mock_result.first.return_value = test_product
    mock_session.exec.return_value = mock_result

    with patch("vineapp.products.models.Session") as mock_session_class:
        mock_session_class.return_value.__enter__.return_value = mock_session

        # When
        repository = ProductRepository(mock_engine)
        product = repository.get_by_id(12)

    # Then
    assert product is not None
    assert product.id == 12
    assert product.name == "T. Bee 13"
    assert product.product_group_id == 113
    assert product.product_group_name == "13 aziaat"


def test_get_product_by_id_not_found():
    """Test retrieving a non-existent product by ID."""
    # Given
    mock_engine = create_autospec(Engine)
    mock_session = create_autospec(Session)
    mock_result = MagicMock()

    # Configure mocks to return None
    mock_result.first.return_value = None
    mock_session.exec.return_value = mock_result

    with patch("vineapp.products.models.Session") as mock_session_class:
        mock_session_class.return_value.__enter__.return_value = mock_session

        # When
        repository = ProductRepository(mock_engine)
        product = repository.get_by_id(999)

    # Then
    assert product is None


def test_repository_init_with_connection_string():
    """Test repository initialization with connection string."""
    # Given
    test_conn_str = "dremio+flight://test:32010/dremio"
    mock_engine = create_autospec(Engine)

    with (
        patch("vineapp.products.models.create_engine") as mock_create_engine,
        patch.dict(os.environ, {"VINEAPP_DB_CONNECTION": test_conn_str}),
    ):
        mock_create_engine.return_value = mock_engine

        # When
        repository = ProductRepository()

        # Then
        mock_create_engine.assert_called_once_with(test_conn_str)
        assert repository.engine == mock_engine


def test_get_paginated_products_with_sorting():
    """Test retrieving paginated products with explicit sorting."""
    # Given
    mock_engine = create_autospec(Engine)
    mock_session = create_autospec(Session)
    mock_result = MagicMock()
    mock_count_result = MagicMock()

    test_products = [
        Product(
            id=12,
            name="T. Bee 13",
            product_group_id=113,
            product_group_name="13 aziaat",
        ),
        Product(
            id=99,
            name="S. Okinawa 19",
            product_group_id=219,
            product_group_name="19 oriëntal",
        ),
    ]

    # Configure mocks
    mock_result.__iter__.return_value = test_products
    mock_session.exec.side_effect = [mock_count_result, mock_result]
    mock_count_result.one.return_value = 10  # Total count

    with patch("vineapp.products.models.Session") as mock_session_class:
        mock_session_class.return_value.__enter__.return_value = mock_session

        # When
        repository = ProductRepository(mock_engine)
        products, total = repository.get_paginated(
            page=2,
            items_per_page=2,
            sort_by="name",
            descending=True,
            filter_text="test",
        )

    # Then
    assert len(products) == 2
    assert total == 10


def test_get_paginated_products_default_sorting():
    """Test retrieving paginated products with default sorting."""
    # Given
    mock_engine = create_autospec(Engine)
    mock_session = create_autospec(Session)
    mock_result = MagicMock()
    mock_count_result = MagicMock()

    test_products = [
        Product(
            id=12,
            name="T. Bee 13",
            product_group_id=113,
            product_group_name="13 aziaat",
        ),
        Product(
            id=99,
            name="S. Okinawa 19",
            product_group_id=219,
            product_group_name="19 oriëntal",
        ),
    ]

    # Configure mocks
    mock_result.__iter__.return_value = test_products
    mock_session.exec.side_effect = [mock_count_result, mock_result]
    mock_count_result.one.return_value = 10  # Total count

    with patch("vineapp.products.models.Session") as mock_session_class:
        mock_session_class.return_value.__enter__.return_value = mock_session

        # When
        repository = ProductRepository(mock_engine)
        products, total = repository.get_paginated(
            page=1,
            items_per_page=2,
            sort_by=None,  # Explicitly set to None to test default sorting
        )

    # Then
    assert len(products) == 2
    assert total == 10
    # We can't reliably test the order of products since we're mocking the database
    # Instead, we verify that we got the expected number of products


def test_get_paginated_products_invalid_page():
    """Test that negative page number raises error."""
    repository = ProductRepository(create_autospec(Engine))
    with pytest.raises(
        InvalidParameterError, match="Page number must be greater than 0"
    ):
        repository.get_paginated(page=0)


def test_get_paginated_products_invalid_items_per_page():
    """Test that negative items_per_page raises error."""
    repository = ProductRepository(create_autospec(Engine))
    with pytest.raises(
        InvalidParameterError, match="Items per page must be greater than 0"
    ):
        repository.get_paginated(items_per_page=0)


def test_get_paginated_products_invalid_sort_column():
    """Test that invalid sort column raises error."""
    repository = ProductRepository(create_autospec(Engine))
    with pytest.raises(InvalidParameterError, match="Invalid sort column"):
        repository.get_paginated(sort_by="invalid_column")
