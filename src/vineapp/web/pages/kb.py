"""Knowledge base page implementation."""

from nicegui import APIRouter, ui

from ...fibery.graphql import get_fibery_client
from ...fibery.models import get_fibery_info
from ..components import frame
from ..components.model_card import display_model_card
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
    LINK_CLASSES,
)


router = APIRouter(prefix="/kb")


@router.page("/")
def kb_page() -> None:
    """Render the knowledge base page."""
    info = get_fibery_info()
    client = get_fibery_client()

    with frame("Knowledge Base"):
        # Display Fibery info using model_card
        display_model_card(info, description_field="description")

        # Get available databases from GraphQL schema
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
                with ui.card().classes(CARD_CLASSES + " border-red-500"):
                    error_msg = response["errors"][0].get("message", "Unknown GraphQL error")
                    ui.label(f"GraphQL Error: {error_msg}").classes("text-red-500")
                return

            if "data" not in response:
                with ui.card().classes(CARD_CLASSES + " border-red-500"):
                    ui.label("Unexpected API response format").classes("text-red-500")
                return

            # Filter for main Fibery database types
            types = response["data"]["__schema"]["types"]
            space_prefix = info._get_type_space_name()
            database_types = [
                t
                for t in types
                if (
                    t["name"].startswith(space_prefix)
                    and t["fields"]
                    and not any(
                        suffix in t["name"] for suffix in ["BackgroundJob", "Operations"]
                    )
                )
            ]

            # Display list of databases
            with ui.card().classes(CARD_CLASSES):
                ui.label("Available Databases").classes(HEADER_CLASSES + " mb-4")

                with ui.column().classes("gap-4"):
                    for type_info in database_types:
                        name = type_info["name"]
                        # Remove space name prefix for cleaner display
                        display_name = name[len(space_prefix):] if name.startswith(space_prefix) else name
                        # Create link for each database to our detail page
                        db_path = display_name.lower().replace(" ", "-")
                        ui.link(display_name, f"/kb/database/{db_path}").classes(LINK_CLASSES)

        except Exception as e:
            with ui.card().classes(CARD_CLASSES + " border-red-500"):
                ui.label(f"Error: {str(e)}").classes("text-red-500")
