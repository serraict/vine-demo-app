"""Tests for web components."""

from pydantic import BaseModel, HttpUrl, computed_field
from nicegui import ui
from nicegui.testing import User

from vineapp.web.components.model_card import display_model_card


class AViewModel(BaseModel):
    """Test model with URL field."""

    name: str
    website: HttpUrl

    @computed_field(return_type=HttpUrl)
    def api_url(self) -> str:  # Changed return type to str to match FiberyInfo
        """Get API URL."""
        base = str(self.website).rstrip("/")
        return f"{base}/api"


async def test_model_card_renders_url_as_link(user: User) -> None:
    """Test that model_card renders URL fields as clickable links."""
    # Given
    test_url = "https://example.com"
    model = AViewModel(
        name="Test Name",
        website=test_url,
    )

    # When
    @ui.page("/test")
    def test_page():
        display_model_card(model)

    await user.open("/test")

    # Then
    await user.should_see("Test Name")  # Regular field should be visible
    await user.should_see("Website")  # Field label should be visible
    await user.should_see("Api Url")  # Computed field label should be visible

    # Verify URLs are rendered as links
    await user.should_see("https://example.com/")  # URL should be visible
    await user.should_see("https://example.com/api")  # Computed URL should be visible
    await user.should_see(kind=ui.link)  # Both URLs should be links
