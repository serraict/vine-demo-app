"""Component for displaying Pydantic models in a card."""

from typing import Optional
from pydantic import BaseModel
from nicegui import ui

from .styles import CARD_CLASSES, HEADER_CLASSES, LABEL_CLASSES, SUBHEADER_CLASSES


def display_model_card(
    model: BaseModel,
    title: Optional[str] = None,
    description_field: Optional[str] = None,
) -> None:
    """Display a Pydantic model in a card format.

    Args:
        model: The Pydantic model instance to display
        title: Optional title to display at the top of the card
        description_field: Optional field name to use as description at the top
    """
    with ui.card().classes(CARD_CLASSES):

        if title:
            ui.label(title).classes(HEADER_CLASSES + " mb-4")
        elif description_field and hasattr(model, description_field):
            ui.label(getattr(model, description_field)).classes(
                HEADER_CLASSES + " mb-4"
            )

        with ui.column().classes("gap-4"):
            for field_name, field in model.model_fields.items():
                # Skip the description field if it's already shown as header
                if field_name == description_field:
                    continue

                with ui.row().classes("gap-2 items-start"):
                    ui.label(field_name.replace("_", " ").title()).classes(
                        LABEL_CLASSES
                    )
                    ui.label(str(getattr(model, field_name))).classes(SUBHEADER_CLASSES)
