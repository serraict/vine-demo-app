"""Article pages and routing."""

from nicegui import APIRouter, ui

from ..components import frame, message


router = APIRouter(prefix="/articles")


@router.page("/")
def index():
    """Render the articles overview page."""
    with frame("Articles"):
        message("Articles")
        ui.label("This page and its subpages are created using an APIRouter.")
        ui.link("Item 1", "/articles/items/1").classes("text-xl text-grey-8")
        ui.link("Item 2", "/articles/items/2").classes("text-xl text-grey-8")
        ui.link("Item 3", "/articles/items/3").classes("text-xl text-grey-8")


@router.page("/items/{item_id}", dark=True)
def item(item_id: str):
    """Render an individual article page.

    Args:
        item_id: The ID of the article to display
    """
    with frame(f"Article -{item_id}-"):
        message(f"Item  #{item_id}")
        ui.link("go back", router.prefix)
