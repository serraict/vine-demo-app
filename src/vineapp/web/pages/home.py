"""Home and about pages implementation."""

from nicegui import APIRouter, ui

from ...app_info import get_application_info
from ..components import frame
from ..components.theme import CARD_CLASSES, HEADER_CLASSES, SUBHEADER_CLASSES, LABEL_CLASSES, LINK_CLASSES, NAV_CARD_CLASSES


# Root router without parameters
root_router = APIRouter()


@root_router.page("/")
def index_page() -> None:
    """Render the homepage."""
    with frame("Homepage"):
        with ui.card().classes(CARD_CLASSES):
            # Header section
            with ui.row().classes("w-full justify-center mb-4"):
                ui.label("Welcome to Vine App").classes(HEADER_CLASSES)

            # Main content section
            with ui.column().classes("w-full items-center gap-4"):
                ui.label("Explore and manage your data pipeline with ease").classes(SUBHEADER_CLASSES)

                # Navigation cards
                with ui.row().classes("w-full gap-4 justify-center mt-4"):
                    with ui.card().classes(NAV_CARD_CLASSES):
                        ui.label("Products").classes(HEADER_CLASSES + " mb-2")
                        ui.label("View and manage your data products").classes(SUBHEADER_CLASSES + " mb-4")
                        ui.link("View Products", "/products").classes(LINK_CLASSES)

                    with ui.card().classes(NAV_CARD_CLASSES):
                        ui.label("About").classes(HEADER_CLASSES + " mb-2")
                        ui.label("Learn more about Vine App").classes(SUBHEADER_CLASSES + " mb-4")
                        ui.link("About", "/about").classes(LINK_CLASSES)


@root_router.page("/about")
def about_page() -> None:
    """Render the about page with application information."""
    info = get_application_info()

    with frame("About"):
        with ui.card().classes(CARD_CLASSES):
            ui.label(info.name).classes(HEADER_CLASSES + " mb-4")

            with ui.column().classes("gap-4"):
                with ui.row().classes("gap-2"):
                    ui.label("Version:").classes(LABEL_CLASSES)
                    ui.label(info.version)

                with ui.row().classes("gap-2 items-start"):
                    ui.label("Description:").classes(LABEL_CLASSES)
                    ui.label(info.description)

                with ui.row().classes("gap-2"):
                    ui.label("Author:").classes(LABEL_CLASSES)
                    ui.label(info.author_email)

                with ui.row().classes("gap-2"):
                    ui.label("Links:").classes(LABEL_CLASSES)
                    ui.link("GitHub", info.project_url, new_tab=True).classes(LINK_CLASSES)
                    ui.link("Documentation", f"{info.project_url}/docs", new_tab=True).classes(LINK_CLASSES)
