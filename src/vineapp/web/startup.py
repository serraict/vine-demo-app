"""Web application startup configuration."""

from nicegui import app

from .pages import articles, home, products


def startup() -> None:
    """Initialize the web application."""
    # Include routers
    app.include_router(articles.router)
    app.include_router(home.router)
    app.include_router(products.router)
