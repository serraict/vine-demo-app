from nicegui import ui


def menu() -> None:
    ui.link("Home", "/").classes(replace="text-white")
    ui.link("Articles", "/articles").classes(replace="text-white")
