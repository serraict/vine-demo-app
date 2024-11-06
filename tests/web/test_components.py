"""Tests for web components."""

from pydantic import BaseModel, HttpUrl
from nicegui import ui
from nicegui.testing import User

from vineapp.web.components.model_card import display_model_card


class AViewModel(BaseModel):
    """Test model with URL field."""

    name: str
    website: HttpUrl


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

    # Verify URL is rendered as a link
    await user.should_see("https://example.com/")  # URL should be visible
    await user.should_see(kind=ui.link)
