"""Navigation menu component."""

from nicegui import ui

from .styles import MENU_LINK_CLASSES


def menu() -> None:
    """Create the navigation menu."""
    with ui.row().classes("gap-4"):
        ui.link("Home", "/").classes(MENU_LINK_CLASSES)
        ui.link("About", "/about").classes(MENU_LINK_CLASSES)
