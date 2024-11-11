"""Models for Fibery data structures."""

from typing import Dict, List, Optional, Union
from urllib.parse import urljoin

from pydantic import BaseModel, HttpUrl


class FiberyEntity(BaseModel):
    """Model representing a Fibery entity."""

    id: str
    name: str
    description: Optional[str] = None


class FiberyInfo(BaseModel):
    """Model representing Fibery environment information."""

    name: str = "Fibery Knowledge Base"
    base_url: HttpUrl
    space_name: str
    databases: List[str] = ["Actions", "Learning"]

    @property
    def kb_url(self) -> HttpUrl:
        """Get the URL to the Fibery knowledge base."""
        return HttpUrl(urljoin(str(self.base_url), f"{self.space_name}/"))

    @property
    def api_url(self) -> HttpUrl:
        """Get the URL to the Fibery API."""
        return HttpUrl(
            urljoin(str(self.base_url), f"api/graphql/space/{self.space_name}")
        )

    @property
    def graphql_url(self) -> HttpUrl:
        """Get the URL to the Fibery GraphQL app."""
        return HttpUrl(
            urljoin(str(self.base_url), f"api/graphql/space/{self.space_name}")
        )


class GraphQLType(BaseModel):
    """Model representing a GraphQL type object."""

    name: str


class FiberyField(BaseModel):
    """Model representing a field in a Fibery type."""

    name: str
    type: Union[GraphQLType, Dict]

    @property
    def type_name(self) -> str:
        """Get the type name from the GraphQL type object."""
        if isinstance(self.type, GraphQLType):
            return self.type.name
        if isinstance(self.type, dict):
            return self.type.get("name", "Unknown")
        return "Unknown"


class FiberySchema(BaseModel):
    """Model representing a Fibery database schema."""

    name: str
    fields: List[FiberyField] = []

    @classmethod
    def from_type_info(cls, type_info: Dict) -> "FiberySchema":
        """Create a FiberySchema instance from GraphQL type info.

        Args:
            type_info: The type info from a GraphQL schema query

        Returns:
            A FiberySchema instance with fields loaded

        Raises:
            ValueError: If type_info has invalid structure
        """
        if not type_info or "name" not in type_info or "fields" not in type_info:
            raise ValueError("Invalid type info structure")

        return cls(
            name=type_info["name"],
            fields=[
                FiberyField(name=f["name"], type=f["type"]) for f in type_info["fields"]
            ],
        )


class FiberyDatabase(BaseModel):
    """Model representing a Fibery database with its schema and entities."""

    name: str
    type_schema: FiberySchema  # Renamed from schema to avoid shadowing
    entities: List[FiberyEntity] = []

    @classmethod
    def from_name(cls, name: str, space_name: str) -> "FiberyDatabase":
        """Create a FiberyDatabase instance from a database name.

        Args:
            name: The name of the database (e.g., 'actions' or 'learning')
            space_name: The Fibery space name to use

        Returns:
            A FiberyDatabase instance with schema and entities loaded

        Raises:
            ValueError: If schema or entities cannot be loaded
        """
        from .graphql import get_fibery_client

        # Convert name to type name (e.g., 'actions' -> '{space_name}Actions')
        type_name = f"{space_name}{name.title()}"

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

        schema_result = client.execute(schema_query)
        if "errors" in schema_result:
            error_msg = schema_result["errors"][0].get(
                "message", "Unknown GraphQL error"
            )
            raise ValueError(f"GraphQL Error: {error_msg}")

        if "data" not in schema_result or "__type" not in schema_result["data"]:
            raise ValueError("Unexpected API response format")

        type_info = schema_result["data"]["__type"]
        if not type_info:
            raise ValueError(f"Type '{type_name}' not found")

        # Create schema from type info
        schema = FiberySchema.from_type_info(type_info)

        # Create instance with schema
        db = cls(name=name, type_schema=schema)

        # Load entities
        db.load_entities()

        return db

    def _build_entities_query(self, field_name: str, limit: int) -> str:
        """Build the GraphQL query for fetching entities.

        Args:
            field_name: The field name to query (e.g., findActions)
            limit: Maximum number of entities to fetch

        Returns:
            str: The GraphQL query string
        """
        return f"""
            query {{
                {field_name} (limit: {limit}) {{
                    id
                    name
                    description {{
                        text
                    }}
                }}
            }}
        """

    def _process_description(self, description: Optional[Dict]) -> Optional[str]:
        """Process a RichField description into plain text.

        Args:
            description: The description field from the GraphQL response

        Returns:
            Optional[str]: The processed description text or None
        """
        if isinstance(description, dict):
            return description.get("text", "")
        return description

    def load_entities(self, limit: int = 5) -> None:
        """Load example entities from the database.

        Args:
            limit: Maximum number of entities to load (must be positive)

        Raises:
            ValueError: If entities cannot be loaded or if limit is invalid
        """
        if limit <= 0:
            raise ValueError("Limit must be a positive integer")

        from .graphql import get_fibery_client
        client = get_fibery_client()

        # Build the field name based on whether the type name ends with 's'
        base_name = self.name.title()
        field_name = f"find{base_name}"
        if not base_name.endswith('s'):
            field_name = f"{field_name}s"

        query = self._build_entities_query(field_name, limit)
        result = client.execute(query)

        if "errors" in result:
            error_msg = result["errors"][0].get("message", "Unknown GraphQL error")
            raise ValueError(f"GraphQL Error: {error_msg}")

        if "data" not in result:
            raise ValueError("Unexpected API response format")

        entities_data = result["data"].get(field_name)
        if not entities_data:
            raise ValueError(f"No entities found for '{self.name}'")

        # Process entities
        self.entities = [
            FiberyEntity(
                id=entity["id"],
                name=entity["name"],
                description=self._process_description(entity.get("description"))
            )
            for entity in entities_data
        ]


def get_fibery_info() -> FiberyInfo:
    """Get information about the Fibery environment from environment variables."""
    import os

    url = os.getenv("VINEAPP_FIBERY_URL")
    if not url:
        raise ValueError("VINEAPP_FIBERY_URL environment variable not set")

    space = os.getenv("VINEAPP_FIBERY_SPACE")
    if not space:
        raise ValueError("VINEAPP_FIBERY_SPACE environment variable not set")

    return FiberyInfo(
        base_url=url,
        space_name=space,
    )
