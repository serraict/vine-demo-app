"""Command line interface for {{cookiecutter.project_name}}."""

import typer
from rich import print
from . import __version__


cli = typer.Typer()


@cli.callback()
def callback() -> None:
    """{{cookiecutter.project_description}}"""


@cli.command()
def version():
    """Show the application version."""
    print(f"[bold]{{cookiecutter.project_name}}[/bold] version: {__version__}")


if __name__ == "__main__":
    cli()
