"""Web interface for the Vine application."""

from nicegui import app, ui

from .web.startup import startup


def init() -> None:
    """Initialize the web application."""
    # Clear any default page layout
    app.on_startup(startup)


if __name__ in {"__main__", "__mp_main__"}:
    init()
    ui.run(title="Serra Vine App")
