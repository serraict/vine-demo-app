"""Database detail page implementation."""

from nicegui import APIRouter, ui
import requests

from ...fibery.graphql import get_fibery_client
from ...fibery.models import FiberyEntity
from ..components import frame
from ..components.model_card import display_model_card
from ..components.styles import (
    CARD_CLASSES,
    HEADER_CLASSES,
)


router = APIRouter(prefix="/kb/database")


@router.page("/{name}")
def database_page(name: str) -> None:
    """Render the database detail page.
    
    Args:
        name: The name of the database (e.g., 'actions' or 'learning')
    """
    with frame(f"{name.title()} Database"):
        try:
            # Convert URL-friendly name back to type name (e.g., 'actions' -> 'PublicActions')
            type_name = f"Public{name.title()}"
            
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
                type_info = schema_result['data']['__type']
                
                # Display schema information
                with ui.card().classes(CARD_CLASSES):
                    ui.label("Schema").classes(HEADER_CLASSES + " mb-4")
                    
                    # Create rows for the table
                    rows = [
                        {'Field': field['name'], 'Type': field['type']['name']}
                        for field in type_info['fields']
                    ]
                    
                    # Create table with schema information
                    ui.table(
                        rows=rows,
                        columns=[
                            {'name': 'Field', 'label': 'Field', 'field': 'Field'},
                            {'name': 'Type', 'label': 'Type', 'field': 'Type'},
                        ]
                    ).classes("w-full")
                
                # Get example entities
                entities_query = f"""
                    query {{
                        find{name.title()} (first: 5) {{
                            id
                            name
                            description
                        }}
                    }}
                """
                entities_result = client.execute(entities_query)
                entities = entities_result['data'][f'find{name.title()}']
                
                # Display example entities
                with ui.card().classes(CARD_CLASSES + " mt-4"):
                    ui.label("Example Entities").classes(HEADER_CLASSES + " mb-4")
                    
                    with ui.column().classes("gap-4"):
                        for entity_data in entities:
                            # Convert dictionary to Pydantic model
                            entity = FiberyEntity(**entity_data)
                            display_model_card(entity)
                            
            except requests.RequestException as e:
                ui.card().classes(CARD_CLASSES + " border-red-500").add(
                    ui.label(f"Error accessing Fibery API: {str(e)}").classes("text-red-500")
                )
                
        except ValueError as e:
            ui.card().classes(CARD_CLASSES + " border-red-500").add(
                ui.label(f"Configuration error: {str(e)}").classes("text-red-500")
            )
