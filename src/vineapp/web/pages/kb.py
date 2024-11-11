"""Knowledge base page implementation."""

from nicegui import APIRouter, ui

from ...fibery.graphql import get_fibery_client
from ...fibery.models import get_fibery_info
from ..components import frame
from ..components.model_card import display_model_card
from ..components.message import message
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
    LINK_CLASSES,
)


router = APIRouter(prefix="/kb")


def _is_database_type(type_info: dict, space_prefix: str) -> bool:
    """Check if a type represents a database.

    Args:
        type_info: The type information from GraphQL schema
        space_prefix: The space name prefix to match

    Returns:
        bool: True if the type represents a database
    """
    return (
        type_info["name"].startswith(space_prefix)
        and type_info["fields"]
        and not any(
            suffix in type_info["name"] for suffix in ["BackgroundJob", "Operations"]
        )
    )


@router.page("/")
def kb_page() -> None:
    """Render the knowledge base page."""
    info = get_fibery_info()
    client = get_fibery_client()

    with frame("Knowledge Base"):
        display_model_card(info, description_field="description")

        query = """
            query {
                __schema {
                    types {
                        name
                        fields {
                            name
                        }
                    }
                }
            }
        """

        try:
            response = client.execute(query)
            if "errors" in response:
                error_msg = response["errors"][0].get(
                    "message", "Unknown GraphQL error"
                )
                message(f"GraphQL Error: {error_msg}")
                return

            if "data" not in response:
                message("Unexpected API response format")
                return

            types = response["data"]["__schema"]["types"]
            space_prefix = info._get_type_space_name()
            database_types = [t for t in types if _is_database_type(t, space_prefix)]

            with ui.card().classes(CARD_CLASSES):
                ui.label("Available Databases").classes(HEADER_CLASSES + " mb-4")

                with ui.column().classes("gap-4"):
                    for type_info in database_types:
                        name = type_info["name"]
                        display_name = (
                            name[len(space_prefix) :]
                            if name.startswith(space_prefix)
                            else name
                        )
                        ui.link(display_name, f"/kb/database/{display_name}").classes(
                            LINK_CLASSES
                        )

        except Exception as e:
            message(f"Error: {str(e)}")
