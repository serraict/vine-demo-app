"""{{cookiecutter.project_description}}"""

try:
    from importlib.metadata import version
    __version__ = version("{{cookiecutter.project_slug}}")
except Exception:
    __version__ = "unknown"
