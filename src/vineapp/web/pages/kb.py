"""Knowledge base page implementation."""

from nicegui import APIRouter, ui

from ...fibery.models import get_fibery_info
from ..components import frame
from ..components.model_card import display_model_card
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
    LINK_CLASSES,
)


router = APIRouter(prefix="/kb")


@router.page("/")
def kb_page() -> None:
    """Render the knowledge base page."""
    info = get_fibery_info()

    with frame("Knowledge Base"):
        # Display Fibery info using model_card
        display_model_card(info, description_field="description")

        # Display list of databases
        with ui.card().classes(CARD_CLASSES):
            ui.label("Available Databases").classes(HEADER_CLASSES + " mb-4")

            with ui.column().classes("gap-4"):
                for db in info.databases:
                    # Create link for each database
                    db_url = f"{info.base_url}/db/{db.lower().replace(' ', '-')}"
                    ui.link(db, db_url, new_tab=True).classes(LINK_CLASSES)
