"""Product data models."""

import os
from typing import List, Optional, Union
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Field, Session, SQLModel, select
from sqlalchemy_dremio.flight import DremioDialect_flight


# Configure Dremio dialect to disable statement caching warning
DremioDialect_flight.supports_statement_cache = False


class Product(SQLModel, table=True):
    """View model for products we make."""

    __tablename__ = "products"
    __table_args__ = {"schema": "Vines"}

    id: int = Field(primary_key=True)
    name: str
    product_group_id: int
    product_group_name: str


class ProductRepository:
    """Read-only repository for product data access."""

    def __init__(self, connection: Optional[Union[str, Engine]] = None):
        """Initialize repository with optional connection string or engine."""
        if isinstance(connection, Engine):
            self.engine = connection
        else:
            conn_str = os.getenv(
                "VINEAPP_DB_CONNECTION", "dremio+flight://localhost:32010/dremio"
            )
            self.engine = create_engine(conn_str)

    def get_all(self) -> List[Product]:
        """Get all products from the data source."""
        with Session(self.engine) as session:
            statement = select(Product).order_by(
                Product.product_group_name, Product.name
            )
            result = session.execute(statement)
            return [row[0] for row in result]
