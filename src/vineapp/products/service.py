"""Product service layer."""

from typing import List
from vineapp.products.models import Product, ProductRepository


class ProductService:
    """Service for accessing product information."""

    def __init__(self, repository: ProductRepository):
        """Initialize service with product repository."""
        self._repository = repository

    def get_all(self) -> List[Product]:
        """Get all products from the repository."""
        return self._repository.get_all()
