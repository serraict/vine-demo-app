"""Theme and layout components."""

from contextlib import contextmanager
from .menu import menu
from nicegui import ui


@contextmanager
def frame(navigation_title: str):
    """Create a themed frame with header and navigation.

    Args:
        navigation_title: The title to display in the navigation bar
    """
    ui.colors(
        brand="#009279",
        primary="#009279",
        secondary="#b5d334",
        accent="#f39c21",
        positive="#b5d334",
        negative="#ad1b11",
        info="#c5b4ff",
        warning="#d38334",
    )

    with ui.header().classes(
        "w-full px-6 py-2 bg-primary flex justify-between items-center"
    ):
        # Left section: App title and navigation
        with ui.row().classes("items-center gap-4"):
            ui.link("Vine App", "/").classes(
                "text-xl font-bold text-white no-underline"
            )
            menu()

        # Right section: Page title
        ui.label(navigation_title).classes("text-lg text-white/90")

    # Main content
    with ui.element("main").classes("w-full flex-grow"):
        with ui.column().classes("w-full items-center p-4"):
            yield
