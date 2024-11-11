"""Database detail page implementation."""

from nicegui import APIRouter, ui
import requests

from ...fibery.graphql import get_fibery_client
from ...fibery.models import FiberyEntity, FiberySchema, get_fibery_info
from ..components import frame
from ..components.model_card import display_model_card
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
)


router = APIRouter(prefix="/kb/database")


def _try_query_with_field(client, query: str) -> tuple[dict, bool]:
    """Try executing a GraphQL query and check if it succeeded.

    Args:
        client: The GraphQL client to use
        query: The query to execute

    Returns:
        Tuple of (result, success) where success indicates if the query succeeded
    """
    result = client.execute(query)
    if "errors" in result:
        return result, False
    return result, True


@router.page("/{name}")
def database_page(name: str) -> None:
    """Render the database detail page.

    Args:
        name: The name of the database (e.g., 'actions' or 'learning')
    """
    with frame(f"{name.title()} Database"):
        try:
            # Get space info and construct type name using actual space name
            info = get_fibery_info()
            type_name = f"{info._get_type_space_name()}{name.title()}"

            # Get schema information using GraphQL
            client = get_fibery_client()
            schema_query = f"""
                query {{
                    __type(name: "{type_name}") {{
                        name
                        fields {{
                            name
                            type {{
                                name
                            }}
                        }}
                    }}
                }}
            """
            try:
                schema_result = client.execute(schema_query)

                # Check for GraphQL errors
                if "errors" in schema_result:
                    error_msg = schema_result["errors"][0].get(
                        "message", "Unknown GraphQL error"
                    )
                    with ui.card().classes(CARD_CLASSES + " border-red-500"):
                        ui.label(f"GraphQL Error: {error_msg}").classes("text-red-500")
                    return

                # Check for expected data structure
                if "data" not in schema_result or "__type" not in schema_result["data"]:
                    with ui.card().classes(CARD_CLASSES + " border-red-500"):
                        ui.label("Unexpected API response format").classes(
                            "text-red-500"
                        )
                    return

                type_info = schema_result["data"]["__type"]
                if not type_info:
                    with ui.card().classes(CARD_CLASSES + " border-red-500"):
                        ui.label(f"Type '{type_name}' not found").classes(
                            "text-red-500"
                        )
                    return

                # Create schema model from type info
                try:
                    schema = FiberySchema.from_type_info(type_info)
                except ValueError as e:
                    with ui.card().classes(CARD_CLASSES + " border-red-500"):
                        ui.label(f"Schema error: {str(e)}").classes("text-red-500")
                    return

                # Display schema information
                with ui.card().classes(CARD_CLASSES):
                    ui.label("Schema").classes(HEADER_CLASSES + " mb-4")

                    # Create rows for the table using schema fields
                    rows = [
                        {"Field": field.name, "Type": field.type_name}
                        for field in schema.fields
                    ]

                    # Create table with schema information
                    ui.table(
                        rows=rows,
                        columns=[
                            {"name": "Field", "label": "Field", "field": "Field"},
                            {"name": "Type", "label": "Type", "field": "Type"},
                        ],
                    ).classes("w-full")

                # Get example entities - try both singular and plural forms
                find_field = f"find{name.title()}"
                entities_query = f"""
                    query {{
                        {find_field} (limit: 5) {{
                            id
                            name
                            description {{
                                text
                            }}
                        }}
                    }}
                """
                result, success = _try_query_with_field(client, entities_query)

                if not success:
                    # Try plural form
                    find_field = f"{find_field}s"
                    entities_query = f"""
                        query {{
                            {find_field} (limit: 5) {{
                                id
                                name
                                description {{
                                    text
                                }}
                            }}
                        }}
                    """
                    result, success = _try_query_with_field(client, entities_query)

                    if not success:
                        error_msg = result["errors"][0].get(
                            "message", "Unknown GraphQL error"
                        )
                        with ui.card().classes(CARD_CLASSES + " border-red-500"):
                            ui.label(f"GraphQL Error: {error_msg}").classes(
                                "text-red-500"
                            )
                        return

                # Check for expected data structure
                if "data" not in result:
                    with ui.card().classes(CARD_CLASSES + " border-red-500"):
                        ui.label("Unexpected API response format").classes(
                            "text-red-500"
                        )
                    return

                if find_field not in result["data"]:
                    with ui.card().classes(CARD_CLASSES + " border-red-500"):
                        ui.label(f"No entities found for '{name}'").classes(
                            "text-red-500"
                        )
                    return

                entities = result["data"][find_field]

                # Display example entities
                with ui.card().classes(CARD_CLASSES + " mt-4"):
                    ui.label("Example Entities").classes(HEADER_CLASSES + " mb-4")

                    with ui.column().classes("gap-4"):
                        for entity_data in entities:
                            # Convert RichField description to plain text
                            description = entity_data.get("description")
                            if isinstance(description, dict):
                                entity_data["description"] = description.get("text", "")
                            # Convert dictionary to Pydantic model
                            entity = FiberyEntity(**entity_data)
                            display_model_card(entity)

            except requests.RequestException as e:
                with ui.card().classes(CARD_CLASSES + " border-red-500"):
                    ui.label(f"Error accessing Fibery API: {str(e)}").classes(
                        "text-red-500"
                    )

        except ValueError as e:
            with ui.card().classes(CARD_CLASSES + " border-red-500"):
                ui.label(f"Configuration error: {str(e)}").classes("text-red-500")
