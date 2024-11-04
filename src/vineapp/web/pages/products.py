"""Products page implementation."""

from typing import List, Dict, Any

from nicegui import APIRouter, ui

from ...products.models import ProductRepository
from ...products.service import ProductService
from ..components import frame


router = APIRouter(prefix="/products")

# Shared table state
table_data = {
    "rows": [],
    "pagination": {
        "rowsPerPage": 10,
        "page": 1,
        "rowsNumber": 0,  # This will actually signal the Quasar component to use server side pagination
    },
}


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

        @ui.refreshable
        def products_table() -> ui.table:
            """Create a refreshable table component."""
            table = ui.table(
                columns=columns,
                rows=table_data["rows"],
                row_key="name",
                pagination=table_data["pagination"],
            )
            table.on("request", handle_pagination)
            return table

        def handle_pagination(event: Dict[str, Any]) -> None:
            """Handle pagination events from the table."""
            # Update pagination state from request
            new_pagination = event.args["pagination"]
            table_data["pagination"].update(new_pagination)

            # Get new page of data
            page = new_pagination.get("page", 1)
            rows_per_page = new_pagination.get("rowsPerPage", 10)

            print(f"Fetching page {page} with {rows_per_page} rows per page")

            products, total = service.get_paginated(
                page=page, items_per_page=rows_per_page
            )

            # Update table data
            table_data["rows"] = [
                {"name": p.name, "product_group_name": p.product_group_name}
                for p in products
            ]
            table_data["pagination"]["rowsNumber"] = total

            # Refresh the table UI
            products_table.refresh()

        # Initial data load
        def load_initial_data() -> None:
            """Load initial data and set total count."""
            products, total = service.get_paginated(page=1, items_per_page=10)
            table_data["rows"] = [
                {"name": p.name, "product_group_name": p.product_group_name}
                for p in products
            ]
            table_data["pagination"]["rowsNumber"] = total
            products_table.refresh()

        # Create table and load data
        table = products_table()
        load_initial_data()

        return table
