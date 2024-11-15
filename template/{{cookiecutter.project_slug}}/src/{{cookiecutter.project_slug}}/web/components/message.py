"""Message display component."""

from nicegui import ui


def message(text: str, type: str = "error") -> None:
    """Display a message notification.

    Args:
        text: The message text to display
        type: The type of message (error, warning, info, success)
    """
    with ui.element("div").classes("w-full flex justify-center"):
        ui.notification(
            text,
            type=type,
            position="top",
            multi_line=True,
            close_button=True,
        ).classes("max-w-md")


def show_error(text: str) -> None:
    """Display an error message.

    Args:
        text: The error message to display
    """
    message(text, type="error")
