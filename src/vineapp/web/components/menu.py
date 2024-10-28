"""Navigation menu component."""

from nicegui import ui


def menu() -> None:
    """Render the navigation menu."""
    ui.link("Home", "/").classes(replace="text-white")
    ui.link("Articles", "/articles").classes(replace="text-white")
