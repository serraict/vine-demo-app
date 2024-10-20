from contextlib import contextmanager

from .menu import menu

from nicegui import ui


@contextmanager
def frame(navigation_title: str):
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
    with ui.header():
        ui.label("Modularization Example").classes("font-bold")
        ui.space()
        ui.label(navigation_title)
        ui.space()
        with ui.row():
            menu()
    with ui.column().classes("absolute-center items-center"):
        yield
