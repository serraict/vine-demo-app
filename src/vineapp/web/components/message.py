"""Message components for displaying errors and other notifications."""

from nicegui import ui
from .styles import CARD_CLASSES


def message(text: str, type: str = "error") -> None:
    """Display a message in a card.

    Args:
        text: The message text to display
        type: The message type ("error" by default)
    """
    if type == "error":
        with ui.card().classes(CARD_CLASSES + " border-red-500"):
            ui.label(text).classes("text-red-500")


def show_error(text: str) -> None:
    """Display an error message.

    Args:
        text: The error message to display
    """
    message(text, type="error")
