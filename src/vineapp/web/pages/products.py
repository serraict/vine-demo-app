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
    products = service.get_all()

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
        rows = [
            {"name": p.name, "product_group_name": p.product_group_name}
            for p in products
        ]
        ui.table(
            columns=columns,
            rows=rows,
            row_key="name",
            pagination=10,
        )
