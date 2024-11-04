"""Tests for web interface."""

from unittest.mock import Mock, patch
from dataclasses import dataclass
from nicegui.testing import User
from nicegui import ui

from vineapp.products.models import Product


@dataclass
class EventArguments:
    """Mock event arguments for testing."""

    args: dict


async def test_products_page_shows_table(user: User) -> None:
    """Test that products page shows a table with product data."""
    with (
        patch("vineapp.web.pages.products.ProductService") as mock_service,
        patch("vineapp.web.pages.products.ProductRepository") as mock_repo,
    ):
        # Given
        mock_repo.return_value = Mock()
        mock_service.return_value = Mock()
        mock_service.return_value.get_paginated.return_value = (
            [
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
            ],
            2,  # total count
        )

        # When
        await user.open("/products")

        # Then
        table = user.find(ui.table).elements.pop()
        assert table.columns == [
            {"name": "name", "label": "Name", "field": "name", "sortable": True},
            {
                "name": "product_group_name",
                "label": "Product Group",
                "field": "product_group_name",
                "sortable": True,
            },
        ]
        assert table.rows == [
            {"name": "T. Bee 13", "product_group_name": "13 aziaat"},
            {"name": "S. Okinawa 19", "product_group_name": "19 oriëntal"},
        ]


async def test_products_page_supports_sorting(user: User) -> None:
    """Test that products can be sorted by name and product group."""
    with (
        patch("vineapp.web.pages.products.ProductService") as mock_service,
        patch("vineapp.web.pages.products.ProductRepository") as mock_repo,
    ):
        # Given
        mock_repo.return_value = Mock()
        service_mock = Mock()
        mock_service.return_value = service_mock

        # Mock initial data load
        service_mock.get_paginated.return_value = (
            [
                Product(
                    id=12,
                    name="T. Bee 13",
                    product_group_id=113,
                    product_group_name="13 aziaat",
                ),
            ],
            3,  # total count
        )

        # When
        await user.open("/products")
        table = user.find(ui.table).elements.pop()

        # Get the request handler
        request_handler = next(
            handler
            for _, handler in table._event_listeners.items()
            if handler.handler.__name__ == "handle_table_request"
        )

        # Simulate sorting by name ascending
        request_handler.handler(
            EventArguments(
                {
                    "pagination": {
                        "page": 1,
                        "rowsPerPage": 10,
                        "sortBy": "name",
                        "descending": False,
                    }
                }
            )
        )

        # Then verify sort by name ascending
        service_mock.get_paginated.assert_called_with(
            page=1, items_per_page=10, sort_by="name", descending=False
        )

        # Simulate sorting by product_group_name descending
        request_handler.handler(
            EventArguments(
                {
                    "pagination": {
                        "page": 1,
                        "rowsPerPage": 10,
                        "sortBy": "product_group_name",
                        "descending": True,
                    }
                }
            )
        )

        # Then verify sort by product_group_name descending
        service_mock.get_paginated.assert_called_with(
            page=1, items_per_page=10, sort_by="product_group_name", descending=True
        )


async def test_products_page_maintains_sort_during_pagination(user: User) -> None:
    """Test that sorting is maintained when changing pages."""
    with (
        patch("vineapp.web.pages.products.ProductService") as mock_service,
        patch("vineapp.web.pages.products.ProductRepository") as mock_repo,
    ):
        # Given
        mock_repo.return_value = Mock()
        service_mock = Mock()
        mock_service.return_value = service_mock

        # Mock initial data load
        service_mock.get_paginated.return_value = (
            [
                Product(
                    id=12,
                    name="T. Bee 13",
                    product_group_id=113,
                    product_group_name="13 aziaat",
                ),
            ],
            30,  # total count
        )

        # When
        await user.open("/products")
        table = user.find(ui.table).elements.pop()

        # Get the request handler
        request_handler = next(
            handler
            for _, handler in table._event_listeners.items()
            if handler.handler.__name__ == "handle_table_request"
        )

        # Set sorting and go to page 2
        request_handler.handler(
            EventArguments(
                {
                    "pagination": {
                        "page": 2,
                        "rowsPerPage": 10,
                        "sortBy": "name",
                        "descending": True,
                    }
                }
            )
        )

        # Then verify sort is maintained
        service_mock.get_paginated.assert_called_with(
            page=2, items_per_page=10, sort_by="name", descending=True
        )
