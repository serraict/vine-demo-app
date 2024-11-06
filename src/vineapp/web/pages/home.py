"""Home and about pages implementation."""

from nicegui import APIRouter, ui

from ...app_info import get_application_info
from ..components import frame


# Root router without parameters
root_router = APIRouter()


@root_router.page("/")
def index_page() -> None:
    """Render the homepage."""
    with frame("Homepage"):
        with ui.card().classes("w-full max-w-3xl mx-auto p-4 shadow-lg"):
            # Header section
            with ui.row().classes("w-full justify-center mb-4"):
                ui.label("Welcome to Vine App").classes(
                    "text-2xl font-bold text-primary"
                )

            # Main content section
            with ui.column().classes("w-full items-center gap-4"):
                ui.label("Explore and manage your data pipeline with ease").classes(
                    "text-lg text-gray-600"
                )

                # Navigation cards
                with ui.row().classes("w-full gap-4 justify-center mt-4"):
                    with ui.card().classes(
                        "w-64 p-4 hover:shadow-lg transition-shadow"
                    ):
                        ui.label("Products").classes(
                            "text-xl font-bold text-primary mb-2"
                        )
                        ui.label("View and manage your data products").classes(
                            "mb-4 text-gray-600"
                        )
                        ui.link("View Products", "/products").classes(
                            "text-accent hover:text-secondary"
                        )

                    with ui.card().classes(
                        "w-64 p-4 hover:shadow-lg transition-shadow"
                    ):
                        ui.label("About").classes("text-xl font-bold text-primary mb-2")
                        ui.label("Learn more about Vine App").classes(
                            "mb-4 text-gray-600"
                        )
                        ui.link("About", "/about").classes(
                            "text-accent hover:text-secondary"
                        )


@root_router.page("/about")
def about_page() -> None:
    """Render the about page with application information."""
    info = get_application_info()

    with frame("About"):
        with ui.card().classes("w-full max-w-3xl mx-auto p-4 shadow-lg"):
            ui.label(info.name).classes("text-2xl font-bold text-primary mb-4")

            with ui.column().classes("gap-4"):
                with ui.row().classes("gap-2"):
                    ui.label("Version:").classes("font-bold text-secondary")
                    ui.label(info.version)

                with ui.row().classes("gap-2 items-start"):
                    ui.label("Description:").classes("font-bold text-secondary")
                    ui.label(info.description)

                with ui.row().classes("gap-2"):
                    ui.label("Author:").classes("font-bold text-secondary")
                    ui.label(info.author_email)

                with ui.row().classes("gap-2"):
                    ui.label("Links:").classes("font-bold text-secondary")
                    ui.link("GitHub", info.project_url, new_tab=True).classes(
                        "text-accent hover:text-secondary"
                    )
                    ui.link(
                        "Documentation", f"{info.project_url}/docs", new_tab=True
                    ).classes("text-accent hover:text-secondary")
