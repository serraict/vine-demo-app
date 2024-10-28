"""Web application startup configuration."""

from nicegui import app, ui

from .pages import articles, home, products


def startup() -> None:
    """Initialize the web application."""
    # Register root page first
    @ui.page("/")  # Direct registration of root page
    def root():
        home.index_page()

    # Include routers
    app.include_router(articles.router)
    app.include_router(home.root_router)
    app.include_router(products.router)
