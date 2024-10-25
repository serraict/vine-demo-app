"""Command line interface for vineapp."""

import typer
from importlib.metadata import metadata, version
from rich.console import Console
from rich.table import Table

from vineapp.products import ProductRepository

app = typer.Typer()
console = Console()


@app.callback()
def callback():
    """Serra Vine CLI application for managing and viewing product data."""


@app.command()
def about():
    """Display application information and version."""
    pkg_metadata = metadata("vineapp")
    app_version = version("vineapp")

    typer.echo(f"Name: {pkg_metadata['Name']}")
    typer.echo(f"Version: {app_version}")
    typer.echo(f"Description: {pkg_metadata['Summary']}")
    typer.echo(f"Author-email: {pkg_metadata['Author-email']}")
    typer.echo(f"Project URL: {pkg_metadata['Project-URL'].split(',')[1].strip()}")


@app.command()
def products():
    """Display a table of all products with their groups."""
    repository = ProductRepository()
    products_list = repository.get_all()

    table = Table(title="Products")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Product Group", style="blue")

    for product in products_list:
        table.add_row(
            str(product.id),
            product.name,
            product.product_group_name,
        )

    console.print(table)


def cli():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    cli()
