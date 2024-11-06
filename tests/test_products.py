"""Tests for product data access."""

import pytest
from vineapp.products.models import ProductRepository, InvalidParameterError
from sqlalchemy.engine import Engine
from unittest.mock import create_autospec


def test_pagination_validation():
    """Test pagination parameter validation."""
    repository = ProductRepository(create_autospec(Engine))

    # Test invalid page numbers
    with pytest.raises(InvalidParameterError, match="Page number must be greater than 0"):
        repository.get_paginated(page=0)
    with pytest.raises(InvalidParameterError, match="Page number must be greater than 0"):
        repository.get_paginated(page=-1)

    # Test invalid items per page
    with pytest.raises(InvalidParameterError, match="Items per page must be greater than 0"):
        repository.get_paginated(items_per_page=0)
    with pytest.raises(InvalidParameterError, match="Items per page must be greater than 0"):
        repository.get_paginated(items_per_page=-5)
