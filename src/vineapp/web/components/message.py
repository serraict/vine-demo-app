"""Message component for displaying headings."""

from nicegui import ui


class message(ui.label):
    """A styled message component based on ui.label."""

    def __init__(self, text: str) -> None:
        """Initialize the message component.

        Args:
            text: The text to display
        """
        super().__init__(text)
        self.classes("text-h4 text-grey-8")
