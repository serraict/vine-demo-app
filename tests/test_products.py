"""Tests for product data access."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from vineapp.products import Product, ProductRepository


@pytest.fixture(name="engine")
def engine_fixture():
    """Create a new database engine for testing."""
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


def test_get_products(engine):
    """Test retrieving products."""
    # Given
    with Session(engine) as session:
        products = [
            Product(
                id=12,
                name="T. Bee 13",
                product_group_id=113,
                product_group_name="13 aziaat",
            ),
            Product(
                id=23,
                name="T. OrangeSen 19",
                product_group_id=319,
                product_group_name="19 sensations",
            ),
            Product(
                id=99,
                name="S. Okinawa 19",
                product_group_id=219,
                product_group_name="19 oriëntal",
            ),
        ]
        for product in products:
            session.add(product)
        session.commit()

    # When
    repository = ProductRepository(engine)
    products = repository.get_all()

    # Then
    assert len(products) == 3
    # Verify products are ordered by product_group_name, then name
    assert [(p.name, p.product_group_name) for p in products] == [
        ("T. Bee 13", "13 aziaat"),
        ("S. Okinawa 19", "19 oriëntal"),
        ("T. OrangeSen 19", "19 sensations"),
    ]
