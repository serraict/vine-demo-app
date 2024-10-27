"""Web interface for the Vine application."""

from . import article_router, theme
from .products.models import ProductRepository
from .products.service import ProductService

from nicegui import app, ui


@ui.page("/")
def index_page() -> None:
    """Render the homepage."""
    with theme.frame("Homepage"):
        ui.label("This is the homepage.")
        ui.link("View Products", "/products")


@ui.page("/products")
def products_page() -> None:
    """Render the products page."""
    repository = ProductRepository()
    service = ProductService(repository)
    products = service.get_all()

    with theme.frame("Products"):
        # Create a table with product data
        columns = [
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


app.include_router(article_router.router)


def main():
    ui.run(title="Serra Vine App")


if __name__ in {"__main__", "__mp_main__"}:
    main()
