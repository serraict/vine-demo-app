"""Tests for core functionality."""

from unittest.mock import create_autospec
from vineapp.products import Product, ProductRepository, ProductService
from vineapp.app_info import ApplicationInfo, get_application_info


def test_product_service_get_all():
    """Test retrieving products through service layer."""
    # Given
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
    mock_repo = create_autospec(ProductRepository)
    mock_repo.get_all.return_value = test_products
    service = ProductService(mock_repo)

    # When
    products = service.get_all()

    # Then
    assert len(products) == 2
    assert [(p.name, p.product_group_name) for p in products] == [
        ("T. Bee 13", "13 aziaat"),
        ("S. Okinawa 19", "19 oriëntal"),
    ]
    mock_repo.get_all.assert_called_once()


def test_get_application_info():
    """Test retrieving application metadata."""
    # When
    info = get_application_info()

    # Then
    assert isinstance(info, ApplicationInfo)
    assert info.name == "vineapp"
    assert info.version  # We don't test exact version as it may change
    assert info.description
    assert info.author_email
    assert info.project_url and info.project_url.startswith("http")
