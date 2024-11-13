"""Tests demonstrating how we'd like to query products using SQLModel.

These tests document the ideal SQLModel query patterns we'd like to use,
but which are currently not supported by Dremio Flight SQL.
See docs/dremio-sqlmodel-limitations.md for details.

To run these tests despite their known failures, set the environment variable:
INCLUDE_DREMIO_LIMITATIONS_TESTS=1

Example:
    INCLUDE_DREMIO_LIMITATIONS_TESTS=1 pytest tests/integration/test_products_ideal.py -v
"""

import os
import pytest
from sqlmodel import Session, select, and_, desc
from vineapp.products import Product


run_limitation_tests = os.getenv("INCLUDE_DREMIO_LIMITATIONS_TESTS") == "1"
skip_reason = "Skipped by default. Set INCLUDE_DREMIO_LIMITATIONS_TESTS=1 to run"


@pytest.mark.skipif(not run_limitation_tests, reason=skip_reason)
def test_get_product_by_name(dremio_engine):
    """Test retrieving a product by name using SQLModel's query pattern.

    This shows how we'd naturally want to filter products using
    SQLModel's clean query syntax with proper parameter binding.
    """
    with Session(dremio_engine) as session:
        # This is how we'd expect to write a simple filter query
        # using SQLModel's intuitive syntax and safe parameter binding
        statement = select(Product).where(Product.name == "T. Bee 13")
        result = session.exec(statement)
        product = result.first()

        assert product is not None
        assert product.name == "T. Bee 13"


@pytest.mark.skipif(not run_limitation_tests, reason=skip_reason)
def test_filter_products_by_multiple_conditions(dremio_engine):
    """Test filtering products with multiple conditions.

    This demonstrates how we'd want to combine multiple filter conditions
    using SQLModel's expressive syntax and proper parameter binding.
    """
    with Session(dremio_engine) as session:
        # This is how we'd naturally write a query with multiple conditions
        statement = select(Product).where(
            and_(Product.product_group_name == "13 aziaat", Product.name.contains("13"))
        )
        result = session.exec(statement)
        products = result.all()

        assert len(products) > 0
        for product in products:
            assert product.product_group_name == "13 aziaat"
            assert "13" in product.name


@pytest.mark.skipif(not run_limitation_tests, reason=skip_reason)
def test_filter_products_by_id_list(dremio_engine):
    """Test filtering products by a list of IDs.

    This demonstrates how we'd want to use the in_ operator to filter
    by multiple values, which is a very common query pattern.
    """
    with Session(dremio_engine) as session:
        # This is how we'd naturally write a query with IN clause
        product_ids = [1, 2, 3]  # Example IDs that should exist
        statement = select(Product).where(Product.id.in_(product_ids))
        result = session.exec(statement)
        products = result.all()

        assert len(products) > 0
        for product in products:
            assert product.id in product_ids


@pytest.mark.skipif(not run_limitation_tests, reason=skip_reason)
def test_dynamic_sort_products(dremio_engine):
    """Test sorting products with dynamic sort direction.

    This demonstrates how we'd want to sort products using SQLModel's
    expressive syntax for dynamic sort fields and directions.
    
    Note: This test actually passes, showing that basic SQL operations
    without parameters work fine with Dremio Flight.
    """
    with Session(dremio_engine) as session:
        # This is how we'd naturally write a query with dynamic sorting
        sort_field = Product.name
        sort_descending = True

        statement = select(Product).order_by(
            desc(sort_field) if sort_descending else sort_field
        )
        result = session.exec(statement)
        products = result.all()

        assert len(products) > 0
        # Verify descending sort
        for i in range(len(products) - 1):
            if (
                products[i].name and products[i + 1].name
            ):  # Handle potential NULL values
                assert products[i].name >= products[i + 1].name
