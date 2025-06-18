"""LLM integration for Slidev Agent."""

from langchain_openai import ChatOpenAI

from slide_agent.config import get_settings


def get_llm() -> ChatOpenAI:
    """Get configured ChatOpenAI instance."""
    settings = get_settings()

    if not settings.openai_api_key:
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY in .env file or environment."
        )

    return ChatOpenAI(
        model=settings.llm.model,
        temperature=settings.llm.temperature,
        max_tokens=settings.llm.max_tokens,
        timeout=settings.llm.timeout,
        api_key=settings.openai_api_key,
    )
