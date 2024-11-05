"""Product data models."""

import os
from typing import List, Optional, Union, Tuple
from sqlalchemy import create_engine, func, Integer, bindparam, desc, text
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

    def get_paginated(
        self,
        page: int = 1,
        items_per_page: int = 10,
        sort_by: Optional[str] = None,
        descending: bool = False,
        filter_text: Optional[str] = None,
    ) -> Tuple[List[Product], int]:
        """Get paginated products from the data source.

        Args:
            page: The page number (1-based)
            items_per_page: Number of items per page
            sort_by: Column name to sort by
            descending: Sort in descending order if True
            filter_text: Optional text to filter products by (case-insensitive)

        Returns:
            Tuple containing list of products for the requested page and total count
        """
        with Session(self.engine) as session:
            # Create base query
            base_query = select(Product)

            # Apply filter if provided
            if filter_text:
                # Create filter expression with direct string interpolation
                pattern = f"%{filter_text}%"
                filter_expr = text(
                    f"lower(name) LIKE lower('{pattern}') OR "
                    f"lower(product_group_name) LIKE lower('{pattern}')"
                )
                base_query = base_query.where(filter_expr)

            # Get total count using COUNT with filters applied
            count_stmt = select(func.count(Product.id)).select_from(
                base_query.subquery()
            )
            total = session.exec(count_stmt).one()

            # Calculate offset
            offset = (page - 1) * items_per_page

            # Apply sorting
            if sort_by:
                column = getattr(Product, sort_by, None)
                if column is not None:
                    if descending:
                        base_query = base_query.order_by(desc(column))
                    else:
                        base_query = base_query.order_by(column)
            else:
                # Default sorting
                base_query = base_query.order_by(
                    Product.product_group_name, Product.name
                )

            # Apply pagination
            query = base_query.limit(
                bindparam("limit", type_=Integer, literal_execute=True)
            ).offset(bindparam("offset", type_=Integer, literal_execute=True))

            # Execute with bound parameters
            result = session.exec(
                query,
                params={
                    "limit": items_per_page,
                    "offset": offset,
                },
            )
            products = list(result)

            return products, total
