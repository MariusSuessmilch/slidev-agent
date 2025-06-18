"""Configuration schemas for different agent workflows."""

from typing import Any

from pydantic import BaseModel, Field


class SlideGenerationConfig(BaseModel):
    """Configuration for slide generation workflow."""

    # Content settings
    default_slide_count: int = Field(default=10, ge=3, le=50)
    default_theme: str = Field(default="the-unnamed")
    default_language: str = Field(default="en")
    default_audience: str = Field(default="general")

    # LLM behavior
    planner_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    writer_temperature: float = Field(default=0.8, ge=0.0, le=2.0)
    reviewer_temperature: float = Field(default=0.3, ge=0.0, le=2.0)

    # Quality settings
    enable_review: bool = Field(default=True)
    max_retries_per_slide: int = Field(default=2, ge=0, le=5)

    # Output settings
    include_speaker_notes: bool = Field(default=True)
    include_transitions: bool = Field(default=True)


class AgentWorkflowConfig(BaseModel):
    """Complete agent workflow configuration."""

    # Workflow settings
    workflow_name: str = Field(default="simple_slide_generation")
    enable_parallel_processing: bool = Field(default=False)

    # Component configs
    slide_generation: SlideGenerationConfig = Field(
        default_factory=SlideGenerationConfig
    )

    # Advanced features (for future milestones)
    enable_web_research: bool = Field(default=False)
    enable_rag_citations: bool = Field(default=False)
    enable_multilang: bool = Field(default=False)


def load_config_from_dict(config_dict: dict[str, Any]) -> AgentWorkflowConfig:
    """Load configuration from dictionary (from YAML/JSON)."""
    return AgentWorkflowConfig(**config_dict)


def get_default_config() -> AgentWorkflowConfig:
    """Get default configuration."""
    return AgentWorkflowConfig()
