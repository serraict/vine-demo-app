"""Home and about pages implementation."""

from nicegui import APIRouter, ui

from ..components import frame
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
    SUBHEADER_CLASSES,
    LINK_CLASSES,
    NAV_CARD_CLASSES,
)


# Root router without parameters
root_router = APIRouter()


@root_router.page("/")
def index_page() -> None:
    """Render the homepage."""
    with frame("Homepage"):
        with ui.card().classes(CARD_CLASSES):
            # Header section
            with ui.row().classes("w-full justify-center mb-4"):
                ui.label("Welcome to {{cookiecutter.project_name}}").classes(
                    HEADER_CLASSES
                )

            # Main content section
            with ui.column().classes("w-full items-center gap-4"):
                ui.label("A Serra Vine application.").classes(SUBHEADER_CLASSES)

                # Navigation cards
                with ui.row().classes("w-full gap-4 justify-center mt-4"):
                    with ui.card().classes(NAV_CARD_CLASSES):
                        ui.label("About").classes(HEADER_CLASSES + " mb-2")
                        ui.label(
                            "Learn more about {{cookiecutter.project_name}}"
                        ).classes(SUBHEADER_CLASSES + " mb-4")
                        ui.link("About", "/about").classes(LINK_CLASSES)


@root_router.page("/about")
def about_page() -> None:
    """Render the about page."""
    with frame("About"):
        with ui.card().classes(CARD_CLASSES):
            ui.label("About {{cookiecutter.project_name}}").classes(
                HEADER_CLASSES + " mb-4"
            )
            ui.label(
                "This is a Serra Vine application created from the template."
            ).classes(SUBHEADER_CLASSES)
