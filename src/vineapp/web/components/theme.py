"""Theme and layout components."""

from contextlib import contextmanager
from .menu import menu
from nicegui import ui


# Common style classes
CARD_CLASSES = "w-full max-w-3xl mx-auto p-4 shadow-lg"
HEADER_CLASSES = "text-2xl font-bold text-primary"
SUBHEADER_CLASSES = "text-lg text-gray-600"
LABEL_CLASSES = "font-bold"
LINK_CLASSES = "text-accent hover:text-secondary"
NAV_CARD_CLASSES = "w-64 p-4 hover:shadow-lg transition-shadow"


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

    with ui.header().classes("items-center justify-between"):
        with ui.row().classes("items-center gap-4"):
            ui.label("Vine App").classes("text-xl font-bold")
            ui.label(navigation_title).classes("text-lg")
        with ui.row():
            menu()
    with ui.column().classes("w-full items-center p-4"):
        yield
