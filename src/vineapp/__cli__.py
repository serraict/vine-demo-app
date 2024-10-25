"""Command line interface for vineapp."""

import typer
from importlib.metadata import metadata, version

app = typer.Typer()


@app.callback()
def callback():
    """Serra Vine CLI application."""


@app.command()
def about():
    """Display information about vineapp."""
    pkg_metadata = metadata("vineapp")
    app_version = version("vineapp")

    typer.echo(f"Name: {pkg_metadata['Name']}")
    typer.echo(f"Version: {app_version}")
    typer.echo(f"Description: {pkg_metadata['Summary']}")
    typer.echo(f"Author-email: {pkg_metadata['Author-email']}")
    typer.echo(f"Project URL: {pkg_metadata['Project-URL'].split(',')[1].strip()}")


def cli():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    cli()
