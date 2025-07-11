"""Domain models for Slidev Agent."""

from enum import Enum
from typing import Any

from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field, model_validator


class SlideType(str, Enum):
    """Types of slides that can be generated."""

    TITLE = "title"
    BULLETS = "bullets"
    CODE = "code"
    DIAGRAM = "diagram"
    QUOTE = "quote"
    IMAGE = "image"
    COMPARISON = "comparison"


class TopicRequest(BaseModel):
    """Request model for slide generation."""

    topic: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="The main topic for the presentation",
    )
    audience: str = Field(
        default="general",
        min_length=1,
        max_length=100,
        description="Target audience level",
    )
    language: str = Field(
        default="de",
        min_length=2,
        max_length=5,
        description="Language for the presentation",
    )
    slide_count: int = Field(
        default=10, ge=3, le=50, description="Number of slides to generate"
    )
    theme: str = Field(
        default="the-unnamed",
        min_length=1,
        max_length=50,
        description="Slidev theme to use",
    )
    additional_context: str | None = Field(
        default=None, max_length=1000, description="Additional context or requirements"
    )

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)


class SlideSpec(BaseModel):
    """Specification for a single slide."""

    title: str = Field(..., min_length=1, max_length=100, description="Slide title")
    slide_type: SlideType = Field(..., description="Type of slide")
    content: str = Field(
        ..., min_length=1, max_length=4000, description="Main content/body of the slide"
    )
    notes: str | None = Field(
        default=None, max_length=1000, description="Speaker notes"
    )
    layout: str | None = Field(
        default=None, max_length=50, description="Slidev layout override"
    )
    transition: str | None = Field(
        default=None, max_length=50, description="Slide transition"
    )
    background: str | None = Field(
        default=None, max_length=200, description="Background image or color"
    )

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)


class SlideDeck(BaseModel):
    """Complete slide deck with metadata."""

    title: str = Field(
        ..., min_length=1, max_length=100, description="Presentation title"
    )
    subtitle: str | None = Field(
        default=None, max_length=200, description="Presentation subtitle"
    )
    author: str | None = Field(default=None, max_length=100, description="Author name")
    theme: str = Field(
        default="the-unnamed", min_length=1, max_length=50, description="Slidev theme"
    )
    slides: list[SlideSpec] = Field(..., min_length=1, description="List of slides")
    fonts: dict[str, str] | None = Field(default=None, description="Font configuration")
    css: str | None = Field(default=None, max_length=10000, description="Custom CSS")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @model_validator(mode="after")
    def validate_slides(self):
        """Validate that the slide deck has proper structure."""
        if not self.slides:
            raise ValueError("Slide deck must contain at least one slide")

        # First slide should be title type
        if self.slides[0].slide_type != SlideType.TITLE:
            raise ValueError("First slide should be of type 'title'")

        return self

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)


class AgentState(BaseModel):
    """State model for the LangGraph agent."""

    request: TopicRequest = Field(..., description="Original request")
    outline: list[dict[str, Any]] | None = Field(
        default=None, description="Generated outline"
    )
    slides: list[SlideSpec] | None = Field(default=None, description="Generated slides")
    deck: SlideDeck | None = Field(default=None, description="Final slide deck")
    error: str | None = Field(default=None, description="Error message if any")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Processing metadata"
    )

    # Better state validation
    model_config = ConfigDict(
        validate_assignment=True, extra="forbid", str_strip_whitespace=True
    )


class SlideOutlineItem(BaseModel):
    """Specification for a single slide in the outline."""

    title: str = Field(
        ..., min_length=1, max_length=100, description="Compelling slide title"
    )
    slide_type: SlideType = Field(
        ..., description="Type of slide: title, bullets, code, comparison, or quote"
    )
    content_summary: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Brief description of slide content",
    )
    key_points: list[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="List of specific key points (1-5 items)",
    )
    notes: str | None = Field(
        default=None, max_length=500, description="Speaker notes or additional context"
    )

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)


@tool
def create_slide_outline(slides: list[dict]) -> dict:
    """Create a detailed outline for a slide presentation.

    Args:
        slides: List of slide dictionaries, each containing:
            - title: str - Compelling slide title
            - slide_type: str - Type: 'title', 'bullets', 'code', 'comparison', 'quote'
            - content_summary: str - Brief description of slide content
            - key_points: list[str] - List of specific key points (1-5 items)
            - notes: str (optional) - Speaker notes or additional context

    Returns:
        Dictionary containing the validated slide outline
    """
    # Validate and return the structured outline
    validated_slides = []

    for slide in slides:
        # Ensure required fields are present
        validated_slide = {
            "title": slide.get("title", "Untitled Slide"),
            "slide_type": slide.get("slide_type", "bullets"),
            "content_summary": slide.get("content_summary", "No description"),
            "key_points": slide.get("key_points", []),
            "notes": slide.get("notes", ""),
        }
        validated_slides.append(validated_slide)

    return {"slides": validated_slides}
