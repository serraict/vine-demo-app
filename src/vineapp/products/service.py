"""Product service layer."""

from typing import List, Tuple, Optional
from vineapp.products.models import Product, ProductRepository


class ProductService:
    """Service for accessing product information."""

    def __init__(self, repository: ProductRepository):
        """Initialize service with product repository."""
        self._repository = repository

    def get_all(self) -> List[Product]:
        """Get all products from the repository."""
        return self._repository.get_all()

    def get_paginated(
        self,
        page: int = 1,
        items_per_page: int = 10,
        sort_by: Optional[str] = None,
        descending: bool = False,
        filter_text: Optional[str] = None,
    ) -> Tuple[List[Product], int]:
        """Get paginated products from the repository.

        Args:
            page: The page number (1-based)
            items_per_page: Number of items per page
            sort_by: Column name to sort by
            descending: Sort in descending order if True
            filter_text: Optional text to filter products by (case-insensitive)

        Returns:
            Tuple containing list of products for the requested page and total count
        """
        return self._repository.get_paginated(
            page=page,
            items_per_page=items_per_page,
            sort_by=sort_by,
            descending=descending,
            filter_text=filter_text,
        )
