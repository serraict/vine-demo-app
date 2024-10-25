"""Product data access layer."""

from typing import List
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Product(SQLModel, table=True):
    """View model for products we make."""

    id: int = Field(primary_key=True)
    name: str
    product_group_id: int
    product_group_name: str


class ProductRepository:
    """Read-only repository for product data access."""

    def __init__(self, engine=None):
        """Initialize repository with optional engine."""
        self.engine = engine or create_engine("sqlite://", echo=False)
        SQLModel.metadata.create_all(self.engine)

    def get_all(self) -> List[Product]:
        """Get all products from the data source."""
        with Session(self.engine) as session:
            statement = select(Product).order_by(
                Product.product_group_name, Product.name
            )
            products = session.exec(statement).all()
            return products
