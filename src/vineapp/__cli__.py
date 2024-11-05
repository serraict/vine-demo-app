"""Command line interface for vineapp."""

import typer
from rich.console import Console
from rich.table import Table

from vineapp.app_info import get_application_info
from vineapp.products import ProductRepository

app = typer.Typer()
console = Console()


@app.callback()
def callback():
    """Serra Vine CLI application for managing and viewing product data."""


@app.command()
def about():
    """Display application information and version."""
    info = get_application_info()

    typer.echo(f"Name: {info.name}")
    typer.echo(f"Version: {info.version}")
    typer.echo(f"Description: {info.description}")
    typer.echo(f"Author-email: {info.author_email}")
    typer.echo(f"Project URL: {info.project_url}")


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
