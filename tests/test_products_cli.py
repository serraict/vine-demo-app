"""Tests for products CLI commands."""

from typer.testing import CliRunner
from vineapp.__cli__ import app
from vineapp.products import Product

runner = CliRunner()


def test_products_command(monkeypatch):
    """Test products list command."""

    # Mock product repository to return test data
    class MockProductRepository:
        def get_all(self):
            return [
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
            ]

    monkeypatch.setattr(
        "vineapp.__cli__.ProductRepository",
        lambda: MockProductRepository(),
    )

    result = runner.invoke(app, ["products"])
    assert result.exit_code == 0
    assert "Products" in result.stdout
    assert "T. Bee 13" in result.stdout
    assert "13 aziaat" in result.stdout
    assert "T. OrangeSen 19" in result.stdout
    assert "19 sensations" in result.stdout
