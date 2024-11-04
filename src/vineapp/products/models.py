"""Product data models."""

import os
from typing import List, Optional, Union, Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlmodel import Field, Session, SQLModel, select
from sqlalchemy_dremio.flight import DremioDialect_flight
from sqlalchemy.dialects import registry


class CustomDremioDialect(DremioDialect_flight):
    """Custom Dremio dialect that implements import_dbapi."""

    supports_statement_cache = False

    @classmethod
    def import_dbapi(cls):
        """Import DBAPI module for Dremio."""
        return DremioDialect_flight.dbapi()


# Register our custom dialect
registry.register("dremio.flight", "vineapp.products.models", "CustomDremioDialect")


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

    def get_paginated(self, page: int = 1, items_per_page: int = 10) -> Tuple[List[Product], int]:
        """Get paginated products from the data source.
        
        Args:
            page: The page number (1-based)
            items_per_page: Number of items per page
            
        Returns:
            Tuple containing list of products for the requested page and total count
        """
        with Session(self.engine) as session:
            # First get total count
            count_stmt = select(Product)
            total = len(session.execute(count_stmt).all())
            
            # Then get paginated results
            offset = (page - 1) * items_per_page
            stmt = text(f"""
                SELECT "Vines".products.id, "Vines".products.name, 
                       "Vines".products.product_group_id, "Vines".products.product_group_name 
                FROM "Vines"."products" 
                ORDER BY "Vines".products.product_group_name, "Vines".products.name
                LIMIT {items_per_page} OFFSET {offset}
            """)
            
            result = session.execute(stmt)
            products = [
                Product(
                    id=row.id,
                    name=row.name,
                    product_group_id=row.product_group_id,
                    product_group_name=row.product_group_name,
                )
                for row in result
            ]
            
            return products, total
