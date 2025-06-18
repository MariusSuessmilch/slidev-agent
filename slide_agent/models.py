"""Domain models for Slidev Agent."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


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

    topic: str = Field(..., description="The main topic for the presentation")
    audience: str = Field(default="general", description="Target audience level")
    language: str = Field(default="en", description="Language for the presentation")
    slide_count: int = Field(
        default=10, ge=3, le=50, description="Number of slides to generate"
    )
    theme: str = Field(default="the-unnamed", description="Slidev theme to use")
    additional_context: Optional[str] = Field(
        default=None, description="Additional context or requirements"
    )


class SlideSpec(BaseModel):
    """Specification for a single slide."""

    title: str = Field(..., description="Slide title")
    slide_type: SlideType = Field(..., description="Type of slide")
    content: str = Field(..., description="Main content/body of the slide")
    notes: Optional[str] = Field(default=None, description="Speaker notes")
    layout: Optional[str] = Field(default=None, description="Slidev layout override")
    transition: Optional[str] = Field(default=None, description="Slide transition")
    background: Optional[str] = Field(
        default=None, description="Background image or color"
    )


class SlideDeck(BaseModel):
    """Complete slide deck with metadata."""

    title: str = Field(..., description="Presentation title")
    subtitle: Optional[str] = Field(default=None, description="Presentation subtitle")
    author: Optional[str] = Field(default=None, description="Author name")
    theme: str = Field(default="the-unnamed", description="Slidev theme")
    slides: list[SlideSpec] = Field(..., description="List of slides")
    fonts: Optional[dict[str, str]] = Field(
        default=None, description="Font configuration"
    )
    css: Optional[str] = Field(default=None, description="Custom CSS")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class AgentState(BaseModel):
    """State model for the LangGraph agent."""

    request: TopicRequest = Field(..., description="Original request")
    outline: Optional[list[dict[str, Any]]] = Field(
        default=None, description="Generated outline"
    )
    slides: Optional[list[SlideSpec]] = Field(
        default=None, description="Generated slides"
    )
    deck: Optional[SlideDeck] = Field(default=None, description="Final slide deck")
    error: Optional[str] = Field(default=None, description="Error message if any")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Processing metadata"
    )
