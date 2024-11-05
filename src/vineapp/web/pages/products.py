"""Products page implementation."""

from typing import List, Dict, Any

from nicegui import APIRouter, ui

from ...products.models import ProductRepository
from ...products.service import ProductService
from ..components import frame


router = APIRouter(prefix="/products")

# Shared table state
table_data = {
    "pagination": {
        "rowsPerPage": 10,
        "page": 1,
        "rowsNumber": 0,  # This will actually signal the Quasar component to use server side pagination
        "sortBy": None,
        "descending": False,
    },
    "filter": "",  # Single filter for searching all fields
}


@router.page("/")
def products_page() -> None:
    """Render the products page with a table of all products."""
    repository = ProductRepository()
    service = ProductService(repository)

    with frame("Products"):
        # Add search input with debounce
        ui.input(
            placeholder="Search products...",
            on_change=lambda e: handle_filter(e),
        ).mark("search")

        columns: List[Dict[str, Any]] = [
            {"name": "name", "label": "Name", "field": "name", "sortable": True},
            {
                "name": "product_group_name",  # name is used as sort key, so preferably the same as field
                "label": "Product Group",
                "field": "product_group_name",
                "sortable": True,
            },
            {"name": "actions", "label": "Actions", "field": "actions"},
        ]

        @ui.refreshable
        def products_table() -> ui.table:
            """Create a refreshable table component."""
            table = ui.table(
                columns=columns,
                rows=table_data["rows"] if "rows" in table_data else [],
                row_key="id",
                pagination=table_data["pagination"],
            )
            table.add_slot(
                "body-cell-actions",
                """
                <q-td :props="props">
                    <q-btn @click="$parent.$emit('view', props)" icon="visibility" flat dense color='primary'/>
                </q-td>
            """,
            )
            table.on("request", handle_table_request)
            table.on("view", handle_view_click)
            return table

        def handle_view_click(e: Any) -> None:
            """Handle click on view button."""
            product_id = e.args.get("key")
            if product_id:
                print(f"Navigating to /products/{product_id}")  # Debug log
                ui.navigate.to(f"/products/{product_id}")

        async def handle_filter(e: Any) -> None:
            """Handle changes to the search filter with debounce."""
            table_data["filter"] = e.value if e.value else ""
            table_data["pagination"]["page"] = 1  # Reset to first page
            load_filtered_data()

        def handle_table_request(event: Dict[str, Any]) -> None:
            """Handle table request events (pagination and sorting)."""
            # Update pagination state from request
            new_pagination = (
                event["pagination"]
                if isinstance(event, dict)
                else event.args["pagination"]
            )
            table_data["pagination"].update(new_pagination)

            # Get new page of data with sorting
            page = new_pagination.get("page", 1)
            rows_per_page = new_pagination.get("rowsPerPage", 10)
            sort_by = new_pagination.get("sortBy")
            descending = new_pagination.get("descending", False)

            print(f"Fetching page {page} with {rows_per_page} rows per page")
            print(f"Sorting by {sort_by} {'descending' if descending else 'ascending'}")
            print(f"Filter: {table_data['filter']}")

            products, total = service.get_paginated(
                page=page,
                items_per_page=rows_per_page,
                sort_by=sort_by,
                descending=descending,
                filter_text=table_data["filter"],  # Pass the filter text to the service
            )

            # Update table data
            table_data["rows"] = [
                {
                    "id": p.id,
                    "name": p.name,
                    "product_group_name": p.product_group_name,
                }
                for p in products
            ]
            table_data["pagination"]["rowsNumber"] = total

            # Refresh the table UI
            products_table.refresh()

        def load_filtered_data() -> None:
            """Load data with current filter and refresh table."""
            handle_table_request({"pagination": table_data["pagination"]})

        # Initial data load
        def load_initial_data() -> None:
            """Load initial data and set total count."""
            products, total = service.get_paginated(page=1, items_per_page=10)
            table_data["rows"] = [
                {
                    "id": p.id,
                    "name": p.name,
                    "product_group_name": p.product_group_name,
                }
                for p in products
            ]
            table_data["pagination"]["rowsNumber"] = total
            products_table.refresh()

        # Create table and load data
        table = products_table()
        load_initial_data()

        return table


@router.page("/{product_id:int}")
def product_detail(product_id: int) -> None:
    """Render the product detail page."""
    repository = ProductRepository()
    service = ProductService(repository)

    with frame("Product Details"):
        product = service.get_by_id(product_id)

        if product:
            with ui.card().classes("w-full").mark("product-details"):
                ui.label(f"Product ID: {product.id}").classes("text-h6")
                ui.label(f"Name: {product.name}").classes("text-h4")
                ui.label(f"Product Group: {product.product_group_name}").classes(
                    "text-h5"
                )
                ui.link("Back to Products", "/products").classes("mt-4")
        else:
            with ui.card().classes("w-full").mark("product-not-found"):
                ui.label("Product not found").classes("text-h4 text-negative")
                ui.link("Back to Products", "/products").classes("mt-4")
