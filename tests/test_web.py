"""Tests for web interface."""

import pytest
from unittest.mock import Mock, patch
from nicegui.testing import User
from vineapp.products.models import Product
from vineapp import __web__


@pytest.mark.module_under_test(__web__)
async def test_homepage_links_to_products(user: User) -> None:
    """Test that homepage contains link to products page."""
    await user.open("/")
    await user.should_see("View Products")
    user.find("View Products").click()
    await user.should_see("Products")


@pytest.mark.module_under_test(__web__)
async def test_products_page_shows_table(user: User) -> None:
    """Test that products page shows a table with product data."""
    with (
        patch("vineapp.__web__.ProductService") as mock_service,
        patch("vineapp.__web__.ProductRepository") as mock_repo,
    ):
        # Given
        mock_repo.return_value = Mock()
        mock_service.return_value = Mock()
        mock_service.return_value.get_all.return_value = [
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

        await user.open("/products")
