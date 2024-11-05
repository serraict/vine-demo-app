"""Tests for product data access."""

from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.engine import Engine
from sqlmodel import Session
from vineapp.products.models import Product, ProductRepository


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
