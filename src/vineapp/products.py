"""Product data access layer."""

from typing import List, Optional, Union
from sqlalchemy.engine import Engine
from sqlmodel import Field, Session, SQLModel, create_engine, select

from vineapp.config import DatabaseConfig


class Product(SQLModel, table=True):
    """View model for products we make."""

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
            config = DatabaseConfig.from_env()
            self.engine = create_engine(
                connection or config.connection_string, echo=False
            )
        SQLModel.metadata.create_all(self.engine)

    def get_all(self) -> List[Product]:
        """Get all products from the data source."""
        with Session(self.engine) as session:
            statement = select(Product).order_by(
                Product.product_group_name, Product.name
            )
            products = session.exec(statement).all()
            return products
