"""Integration tests for Dremio connection and product retrieval."""
from sqlalchemy.exc import SQLAlchemyError
from vineapp.products import Product, ProductRepository


def test_can_connect_to_dremio(dremio_engine):
    """Test that we can establish a connection to Dremio."""
    with dremio_engine.connect() as connection:
        result = connection.execute("SELECT 1").scalar()
        assert result == 1


def test_can_retrieve_products(product_repository: ProductRepository):
    """Test that we can retrieve products from Dremio."""
    products = product_repository.get_all()
    
    assert len(products) > 0
    for product in products:
        assert isinstance(product, Product)
        assert product.id is not None
        assert product.name
        assert product.product_group_id is not None
        assert product.product_group_name


def test_handles_connection_error(dremio_engine):
    """Test that connection errors are handled gracefully."""
    # Force a connection error by disposing the engine
    dremio_engine.dispose()
    
    try:
        with dremio_engine.connect():
            pass
    except SQLAlchemyError as e:
        assert "Connection" in str(e)
