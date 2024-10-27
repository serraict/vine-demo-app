"""Application metadata information."""

from dataclasses import dataclass
from importlib.metadata import metadata, version


@dataclass
class ApplicationInfo:
    """Application metadata information."""

    name: str
    version: str
    description: str
    author_email: str
    project_url: str


def get_application_info() -> ApplicationInfo:
    """Get application metadata information."""
    pkg_metadata = metadata("vineapp")
    app_version = version("vineapp")

    return ApplicationInfo(
        name=pkg_metadata["Name"],
        version=app_version,
        description=pkg_metadata["Summary"],
        author_email=pkg_metadata["Author-email"],
        project_url=pkg_metadata["Project-URL"].split(",")[1].strip(),
    )
