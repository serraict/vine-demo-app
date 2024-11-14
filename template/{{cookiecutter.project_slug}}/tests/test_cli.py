"""Test the command line interface."""

from typer.testing import CliRunner
from {{cookiecutter.project_slug}}.__cli__ import cli
from {{cookiecutter.project_slug}} import __version__

runner = CliRunner()


def test_version():
    """Test the version command."""
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout
