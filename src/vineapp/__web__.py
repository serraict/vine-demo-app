"""Web interface for the Vine application."""

from typing import List, Dict, Any

from . import article_router, theme
from .app_info import get_application_info
from .products.models import ProductRepository
from .products.service import ProductService

from nicegui import app, ui


@ui.page("/")
def index_page() -> None:
    """Render the homepage."""
    with theme.frame("Homepage"):
        ui.label("This is the homepage.")
        with ui.row():
            ui.link("View Products", "/products")
            ui.link("About", "/about")


@ui.page("/about")
def about_page() -> None:
    """Render the about page with application information."""
    info = get_application_info()

    with theme.frame("About"):
        with ui.card().classes("w-full max-w-3xl mx-auto p-4"):
            ui.label(info.name).classes("text-2xl font-bold mb-4")

            with ui.row().classes("gap-1"):
                ui.label("Version:").classes("font-bold")
                ui.label(info.version)

            with ui.row().classes("gap-1 items-start"):
                ui.label("Description:").classes("font-bold")
                ui.label(info.description)

            with ui.row().classes("gap-1"):
                ui.label("Author:").classes("font-bold")
                ui.label(info.author_email)

            with ui.row().classes("gap-1"):
                ui.label("Links:").classes("font-bold")
                ui.link("GitHub", info.project_url, new_tab=True)
                ui.link("Documentation", f"{info.project_url}/docs", new_tab=True)


@ui.page("/products")
def products_page() -> None:
    """Render the products page with a table of all products."""
    repository = ProductRepository()
    service = ProductService(repository)
    products = service.get_all()

    with theme.frame("Products"):
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


app.include_router(article_router.router)


def main() -> None:
    """Run the web application."""
    ui.run(title="Serra Vine App")


if __name__ in {"__main__", "__mp_main__"}:
    main()
