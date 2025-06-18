"""LLM integration for Slidev Agent."""

from langchain_openai import ChatOpenAI

from slide_agent.config import get_settings


def get_llm() -> ChatOpenAI:
    """Get configured ChatOpenAI instance."""
    settings = get_settings()

    return ChatOpenAI(
        model=settings.llm.model,
        temperature=settings.llm.temperature,
        max_tokens=settings.llm.max_tokens,
        timeout=settings.llm.timeout,
        api_key=settings.openai_api_key,
    )
