"""Products page implementation."""

from typing import List, Dict, Any

from nicegui import APIRouter, ui

from ...products.models import ProductRepository
from ...products.service import ProductService
from ..components import frame


router = APIRouter(prefix="/products")


@router.page("/")
def products_page() -> None:
    """Render the products page with a table of all products."""
    repository = ProductRepository()
    service = ProductService(repository)

    with frame("Products"):
        columns: List[Dict[str, Any]] = [
            {"name": "name", "label": "Name", "field": "name", "sortable": True},
            {
                "name": "group",
                "label": "Product Group",
                "field": "product_group_name",
                "sortable": True,
            },
        ]

        # Get initial page of data
        products, total = service.get_paginated(page=1, items_per_page=10)
        rows = [
            {"name": p.name, "product_group_name": p.product_group_name}
            for p in products
        ]

        # Create table with pagination
        table = ui.table(
            columns=columns,
            rows=rows,
            row_key="name",
            pagination={
                "page": 1,
                "rowsPerPage": 10,
                "rowsPerPageOptions": [10, 25, 50],
                "rowsNumber": total,
            },
        )

        # Define handler function
        def handle_pagination(event: Dict[str, Any]) -> None:
            """Handle pagination events from the table."""
            page = event.value.get("page", 1)
            rows_per_page = event.value.get("rowsPerPage", 10)

            print(f"Fetching page {page} with {rows_per_page} rows per page")

            # Get new page of data
            products, total = service.get_paginated(
                page=page, items_per_page=rows_per_page
            )

            # Update table with new data
            table.rows = [
                {"name": p.name, "product_group_name": p.product_group_name}
                for p in products
            ]
            table.update()

        # Store handler for testing
        table.handle_pagination = handle_pagination  # type: ignore

        # Bind handler to table
        table.on_pagination_change(handle_pagination)

        return table
