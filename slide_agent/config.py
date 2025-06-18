"""Configuration management for Slidev Agent."""

import os
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class LLMConfig(BaseModel):
    """Configuration for LLM integration."""

    model: str = Field(default="gpt-4o", description="OpenAI model to use")
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Temperature for generation"
    )
    max_tokens: Optional[int] = Field(
        default=None, description="Maximum tokens to generate"
    )
    timeout: int = Field(default=60, description="Request timeout in seconds")


class TracingConfig(BaseModel):
    """Configuration for LangSmith tracing."""

    enabled: bool = Field(default=True, description="Whether to enable tracing")
    project_name: str = Field(default="slidev", description="LangSmith project name")
    session_id: Optional[str] = Field(
        default=None, description="Session ID for grouping traces"
    )


class AgentConfig(BaseModel):
    """Configuration for the agent behavior."""

    max_retries: int = Field(
        default=3, description="Maximum retries for failed operations"
    )
    enable_research: bool = Field(
        default=False, description="Enable web research (future feature)"
    )
    output_format: str = Field(
        default="markdown", description="Output format for slides"
    )


class Settings(BaseSettings):
    """Main settings class that loads from environment."""

    # API Keys
    openai_api_key: str = Field(default="", description="OpenAI API key")
    langchain_api_key: Optional[str] = Field(
        default=None, description="LangSmith API key", alias="langsmith_api_key"
    )

    # LangSmith Configuration
    langchain_tracing_v2: bool = Field(
        default=True, description="Enable LangSmith tracing"
    )
    langchain_project: str = Field(
        default="slidev-agent", description="LangSmith project name"
    )
    langchain_endpoint: str = Field(
        default="https://api.smith.langchain.com", description="LangSmith endpoint"
    )

    # Component Configurations
    llm: LLMConfig = Field(default_factory=LLMConfig)
    tracing: TracingConfig = Field(default_factory=TracingConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_nested_delimiter": "__",
        "extra": "ignore",
    }


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


def setup_tracing() -> None:
    """Setup LangSmith tracing environment variables."""
    settings = get_settings()

    if settings.langchain_api_key:
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key

    os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2).lower()
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
    os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
