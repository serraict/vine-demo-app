from . import article_router
from . import theme

from nicegui import app, ui


@ui.page("/")
def index_page() -> None:
    with theme.frame("Homepage"):
        ui.label("This is the homepage.")


app.include_router(article_router.router)
ui.run(title="Modularization Example")
