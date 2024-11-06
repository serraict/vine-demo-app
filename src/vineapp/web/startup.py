"""Web application startup configuration."""

from nicegui import app

from .pages import home, products


def startup() -> None:
    """Initialize the web application."""
    # Include routers
    app.include_router(home.root_router)
    app.include_router(products.router)
