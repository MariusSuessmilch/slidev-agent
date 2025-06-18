"""LangGraph agent workflow for Slidev slide generation."""

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from slide_agent.config import setup_tracing
from slide_agent.llm import get_llm
from slide_agent.models import AgentState, SlideDeck, SlideSpec, SlideType, TopicRequest


def planner_node(state: AgentState) -> dict[str, Any]:
    """Plan the slide structure based on the topic request."""
    llm = get_llm()

    prompt = f"""
    You are a presentation planner. Create an outline for a {state.request.slide_count}-slide presentation about: {state.request.topic}

    Audience: {state.request.audience}
    Language: {state.request.language}

    Additional context: {state.request.additional_context or 'None'}

    Return a JSON array of slide objects with this structure:
    [
        {{
            "title": "Slide title",
            "slide_type": "title|bullets|code|diagram|quote|image|comparison",
            "content_points": ["key point 1", "key point 2", "..."]
        }}
    ]

    Make sure to include:
    - A compelling title slide
    - 2-3 main content sections
    - Clear learning objectives
    - A conclusion/summary slide
    """

    response = llm.invoke(
        [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Create outline for: {state.request.topic}"),
        ]
    )

    # For now, return a simple mock outline - in M3 we'll parse the LLM response
    outline = [
        {
            "title": f"Introduction to {state.request.topic}",
            "slide_type": "title",
            "content_points": ["Overview of the topic"],
        },
        {
            "title": "Key Concepts",
            "slide_type": "bullets",
            "content_points": ["Concept 1", "Concept 2", "Concept 3"],
        },
        {
            "title": "Summary",
            "slide_type": "bullets",
            "content_points": ["Recap", "Next steps"],
        },
    ]

    return {
        "outline": outline,
        "metadata": {
            "planner_response": response.content,
            "planned_slides": len(outline),
        },
    }


def slide_writer_node(state: AgentState) -> dict[str, Any]:
    """Generate individual slides based on the outline."""
    if not state.outline:
        return {"error": "No outline available for slide generation"}

    llm = get_llm()
    slides = []

    for slide_data in state.outline:
        slide_type = SlideType(slide_data["slide_type"])

        prompt = f"""
        Create slide content for a {slide_type.value} slide.
        Title: {slide_data["title"]}
        Content points: {slide_data["content_points"]}

        Topic context: {state.request.topic}
        Audience: {state.request.audience}

        Generate appropriate content for this slide type.
        Keep it concise and engaging.
        """

        response = llm.invoke(
            [
                SystemMessage(content=prompt),
                HumanMessage(content=f"Generate content for: {slide_data['title']}"),
            ]
        )

        slide = SlideSpec(
            title=slide_data["title"],
            slide_type=slide_type,
            content=response.content,
            notes=f"Generated for topic: {state.request.topic}",
        )
        slides.append(slide)

    return {"slides": slides}


def reviewer_node(state: AgentState) -> dict[str, Any]:
    """Review and finalize the slide deck."""
    if not state.slides:
        return {"error": "No slides available for review"}

    llm = get_llm()

    # Create the final deck
    deck = SlideDeck(
        title=f"Presentation: {state.request.topic}",
        subtitle=f"For {state.request.audience} audience",
        theme=state.request.theme,
        slides=state.slides,
        metadata={
            "generated_by": "slidev-agent",
            "topic": state.request.topic,
            "slide_count": len(state.slides),
            "language": state.request.language,
        },
    )

    # Simple quality check
    review_prompt = f"""
    Review this slide deck outline:
    Topic: {deck.title}
    Number of slides: {len(deck.slides)}
    Slide titles: {[slide.title for slide in deck.slides]}

    Rate the quality and provide brief feedback.
    """

    review = llm.invoke(
        [
            SystemMessage(content=review_prompt),
            HumanMessage(content="Please review this presentation structure."),
        ]
    )

    return {
        "deck": deck,
        "metadata": {
            **state.metadata,
            "review_feedback": review.content,
            "final_slide_count": len(deck.slides),
        },
    }


def create_agent_graph() -> StateGraph:
    """Create and configure the LangGraph workflow."""
    # Setup tracing
    setup_tracing()

    # Create the workflow
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("slide_writer", slide_writer_node)
    workflow.add_node("reviewer", reviewer_node)

    # Define the flow
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "slide_writer")
    workflow.add_edge("slide_writer", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()


def run_agent(topic_request: TopicRequest) -> AgentState:
    """Run the slide generation agent workflow."""
    graph = create_agent_graph()

    initial_state = AgentState(
        request=topic_request, metadata={"session_id": "simple-run"}
    )

    result = graph.invoke(initial_state)
    return result
