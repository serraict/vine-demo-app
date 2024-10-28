"""Tests for web interface."""

from unittest.mock import Mock, patch
from nicegui.testing import User
from nicegui import ui

from vineapp.products.models import Product


async def test_products_page_shows_table(user: User) -> None:
    """Test that products page shows a table with product data."""
    with (
        patch("vineapp.web.pages.products.ProductService") as mock_service,
        patch("vineapp.web.pages.products.ProductRepository") as mock_repo,
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

        # When
        await user.open("/products")

        # Then
        table = user.find(ui.table).elements.pop()
        assert table.columns == [
            {"name": "name", "label": "Name", "field": "name", "sortable": True},
            {
                "name": "group",
                "label": "Product Group",
                "field": "product_group_name",
                "sortable": True,
            },
        ]
        assert table.rows == [
            {"name": "T. Bee 13", "product_group_name": "13 aziaat"},
            {"name": "S. Okinawa 19", "product_group_name": "19 oriëntal"},
        ]
