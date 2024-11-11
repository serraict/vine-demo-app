"""Database detail page implementation."""

from nicegui import APIRouter, ui
from typing import Optional

from ...fibery.graphql import get_fibery_client
from ...fibery.models import FiberyEntity, FiberySchema, get_fibery_info
from ..components import frame
from ..components.model_card import display_model_card
from ..components.message import message
from ..components.theme import with_error_handling
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
)


router = APIRouter(prefix="/kb/database")


def _build_schema_query(type_name: str) -> str:
    """Build GraphQL query for schema information.

    Args:
        type_name: The name of the type to query

    Returns:
        str: The GraphQL query
    """
    return f"""
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


def _build_entities_query(field_name: str) -> str:
    """Build GraphQL query for entities.

    Args:
        field_name: The field name to query (e.g., findActions)

    Returns:
        str: The GraphQL query
    """
    return f"""
        query {{
            {field_name} (limit: 5) {{
                id
                name
                description {{
                    text
                }}
            }}
        }}
    """


def _display_schema(schema: FiberySchema) -> None:
    """Display schema information in a card.

    Args:
        schema: The schema to display
    """
    with ui.card().classes(CARD_CLASSES):
        ui.label("Schema").classes(HEADER_CLASSES + " mb-4")
        rows = [
            {"Field": field.name, "Type": field.type_name} for field in schema.fields
        ]
        ui.table(
            rows=rows,
            columns=[
                {"name": "Field", "label": "Field", "field": "Field"},
                {"name": "Type", "label": "Type", "field": "Type"},
            ],
        ).classes("w-full")


def _display_entities(entities: list) -> None:
    """Display entities in a card.

    Args:
        entities: List of entities to display
    """
    with ui.card().classes(CARD_CLASSES + " mt-4"):
        ui.label("Example Entities").classes(HEADER_CLASSES + " mb-4")
        with ui.column().classes("gap-4"):
            for entity_data in entities:
                description = entity_data.get("description")
                if isinstance(description, dict):
                    entity_data["description"] = description.get("text", "")
                entity = FiberyEntity(**entity_data)
                display_model_card(entity)


def _get_schema(client, type_name: str) -> Optional[FiberySchema]:
    """Get schema information from Fibery.

    Args:
        client: The GraphQL client to use
        type_name: The name of the type to query

    Returns:
        Optional[FiberySchema]: Schema if found, None if error
    """
    schema_result = client.execute(_build_schema_query(type_name))
    if "errors" in schema_result:
        error_msg = schema_result["errors"][0].get("message", "Unknown GraphQL error")
        message(f"GraphQL Error: {error_msg}")
        return None

    if "data" not in schema_result or "__type" not in schema_result["data"]:
        message("Unexpected API response format")
        return None

    type_info = schema_result["data"]["__type"]
    if not type_info:
        message(f"Type '{type_name}' not found")
        return None

    try:
        return FiberySchema.from_type_info(type_info)
    except ValueError as e:
        message(f"Schema error: {str(e)}")
        return None


def _get_entities(client, name: str) -> Optional[list]:
    """Get entities from Fibery.

    Args:
        client: The GraphQL client to use
        name: The name of the database

    Returns:
        Optional[list]: List of entities if found, None if error
    """
    # Try singular form first
    find_field = f"find{name}"
    result = client.execute(_build_entities_query(find_field))
    if "errors" not in result and "data" in result and find_field in result["data"]:
        return result["data"][find_field]

    # Try plural form
    find_field = f"{find_field}s"
    result = client.execute(_build_entities_query(find_field))
    if "errors" not in result and "data" in result and find_field in result["data"]:
        return result["data"][find_field]

    if "errors" in result:
        error_msg = result["errors"][0].get("message", "Unknown GraphQL error")
        message(f"GraphQL Error: {error_msg}")
    elif "data" not in result:
        message("Unexpected API response format")
    else:
        message(f"No entities found for '{name}'")
    return None


@router.page("/{name}")
@with_error_handling
def database_page(name: str) -> None:
    """Render the database detail page.

    Args:
        name: The name of the database (e.g., 'Actie' or 'Werkdocument')
    """
    info = get_fibery_info()
    client = get_fibery_client()
    type_name = f"{info._get_type_space_name()}{name}"

    with frame(f"{name} Database"):
        schema = _get_schema(client, type_name)
        if schema:
            _display_schema(schema)
            entities = _get_entities(client, name)
            if entities:
                _display_entities(entities)
