"""Home and about pages implementation."""

from nicegui import APIRouter, ui

from ...app_info import get_application_info
from ..components import frame


router = APIRouter(prefix="/home")


@router.page("/")
def index_page():
    """Render the homepage."""
    with frame("Homepage"):
        # Create content
        content = ui.column().classes("items-center")
        with content:
            ui.label("This is the homepage").classes("text-xl")
            with ui.row().classes("gap-4 mt-4"):
                ui.link("View Products", "/products").classes("text-lg")
                ui.link("About", "/home/about").classes("text-lg")


@router.page("/about")
def about_page():
    """Render the about page with application information."""
    info = get_application_info()

    with frame("About"):
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
