"""Test the CLI interface."""

from typer.testing import CliRunner
from vineapp.__cli__ import app
from importlib.metadata import metadata, version

runner = CliRunner()


def test_about_command():
    """Test that the about command displays the correct information."""
    result = runner.invoke(app, ["about"])
    pkg_metadata = metadata("vineapp")

    assert result.exit_code == 0
    assert f"Name: {pkg_metadata['Name']}" in result.stdout
    assert f"Version: {version('vineapp')}" in result.stdout
    assert f"Description: {pkg_metadata['Summary']}" in result.stdout
    assert f"Author-email: {pkg_metadata['Author-email']}" in result.stdout
    assert f"Project URL: {pkg_metadata['Project-URL'].split(',')[1].strip()}" in result.stdout
