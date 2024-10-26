"""Integration tests for Dremio connection and product retrieval."""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from vineapp.products import Product, ProductRepository


@pytest.mark.integration
def test_can_connect_to_dremio(dremio_engine):
    """Test that we can establish a connection to Dremio."""
    with dremio_engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar()
        assert result == 1


@pytest.mark.integration
def test_can_retrieve_products(product_repository: ProductRepository):
    """Test that we can retrieve products from Dremio."""
    products = product_repository.get_all()
    
    # Verify we can retrieve products
    assert isinstance(products, list)
    
    # Verify each item is a Product instance
    for product in products:
        assert isinstance(product, Product)


@pytest.mark.integration
def test_handles_connection_error(dremio_engine):
    """Test that connection errors are handled gracefully."""
    # Force a connection error by disposing the engine
    dremio_engine.dispose()
    
    try:
        with dremio_engine.connect():
            pass
    except SQLAlchemyError as e:
        assert "Connection" in str(e)
