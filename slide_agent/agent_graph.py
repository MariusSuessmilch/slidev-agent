"""LangGraph agent workflow for Slidev slide generation."""

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from slide_agent.config import setup_tracing
from slide_agent.llm import get_llm
from slide_agent.models import AgentState, SlideDeck, SlideSpec, SlideType, TopicRequest
from slide_agent.writers import FilesystemWriter


def planner_node(state: AgentState) -> dict[str, Any]:
    """Plan the slide structure based on the topic request."""
    llm = get_llm()

    prompt = f"""
    You are an expert presentation planner. Create a detailed outline for a {state.request.slide_count}-slide presentation about: {state.request.topic}

    Audience: {state.request.audience}
    LANGUAGE: {state.request.language} - ALL TITLES AND CONTENT MUST BE IN THIS LANGUAGE!
    Additional context: {state.request.additional_context or 'None'}

    Return ONLY a valid JSON array with this exact structure:
    [
        {{
            "title": "Compelling slide title",
            "slide_type": "title|bullets|code|comparison|quote",
            "content_summary": "Brief description of slide content",
            "key_points": ["specific point 1", "specific point 2", "specific point 3"],
            "notes": "Speaker notes or additional context"
        }}
    ]

    Slide type guidelines:
    - "title": Opening slide with topic introduction
    - "bullets": Key concepts, benefits, explanations with bullet points  
    - "code": Programming examples, syntax demonstrations
    - "comparison": Before/after, pros/cons, alternatives
    - "quote": Summary, conclusion, or inspirational content

    For "{state.request.topic}" and "{state.request.audience}" audience, create exactly {state.request.slide_count} slides:
    1. Start with a title slide
    2. Include practical examples relevant to the audience
    3. Use code slides for technical topics
    4. End with summary/conclusion

    Respond with ONLY the JSON array, no additional text.
    """

    response = llm.invoke(
        [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Create outline for: {state.request.topic}"),
        ]
    )

    # Parse JSON response from LLM
    try:
        import json
        # Extract JSON from response
        response_text = response.content.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()

        outline = json.loads(response_text)

        # Convert to expected format
        for slide in outline:
            if "content_points" not in slide and "key_points" in slide:
                slide["content_points"] = slide["key_points"]
    except (json.JSONDecodeError, KeyError):
        # Fallback to topic-specific outline
        if "python" in state.request.topic.lower() and "funktion" in state.request.topic.lower():
            outline = [
                {
                    "title": "Python Funktionen für Schüler",
                    "slide_type": "title",
                    "content_points": ["Einführung in Python Funktionen", "Warum Funktionen wichtig sind"],
                },
                {
                    "title": "Was ist eine Funktion?",
                    "slide_type": "bullets",
                    "content_points": ["Definition einer Funktion", "Warum verwenden wir Funktionen?", "Beispiele aus dem Alltag"],
                },
                {
                    "title": "Erste Funktion erstellen",
                    "slide_type": "code",
                    "content_points": ["def-Schlüsselwort", "Funktionsname und Parameter", "Funktionskörper"],
                },
                {
                    "title": "Parameter und Argumente",
                    "slide_type": "code",
                    "content_points": ["Was sind Parameter?", "Argumente übergeben", "Beispiele mit verschiedenen Parametern"],
                },
                {
                    "title": "Return-Werte",
                    "slide_type": "code",
                    "content_points": ["return-Statement", "Rückgabewerte verwenden", "Funktionen mit und ohne return"],
                },
                {
                    "title": "Praktische Übungen",
                    "slide_type": "bullets",
                    "content_points": ["Einfache Mathematik-Funktionen", "Text-Verarbeitung", "Interaktive Programme"],
                },
                {
                    "title": "Zusammenfassung",
                    "slide_type": "quote",
                    "content_points": ["Was haben wir gelernt?", "Nächste Schritte", "Übungsaufgaben"],
                },
            ]
        else:
            # Generic fallback
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
        LANGUAGE: {state.request.language} - ALL CONTENT MUST BE IN THIS LANGUAGE!

        IMPORTANT CONTENT LIMITS:
        - Maximum 10 lines per slide total
        - Maximum 5 bullet points per slide
        - Each bullet point: maximum 1 line of text
        - NO nested bullet points (no sub-bullets with indentation)
        - Keep explanations concise and focused
        - Avoid lengthy paragraphs
        - Use clear, simple language
        
        For code slides: 
        - Include only essential code snippets (max 10 lines)
        - CRITICAL: Format code blocks correctly. NEVER concatenate language with code!
        - Use ONLY these exact language names: python, javascript, java, cpp, c, sql, bash, html, css, json, yaml, xml
        - ALWAYS use this exact format: ```python<newline>def function():<newline>    pass<newline>```
        - NEVER write: ```pythondef or ```python# or ```pythonimport
        - ALWAYS write: ```python<newline>def or ```python<newline># or ```python<newline>import
        For title slides: 
        - Use simple, single-level bullet points only
        - NO nested or indented sub-bullets
        - Maximum 5 simple bullet points
        - Each bullet should be one clear, short statement
        - Focus on overview, importance, and what audience will learn
        For bullet slides: Focus on key concepts only
        For comparison slides: Keep comparisons brief and clear
        For quote slides: 
        - Create an inspiring summary or conclusion
        - Use format: Clear statements without quotation marks
        - End with a memorable phrase or call-to-action
        - NO code blocks, NO complex formatting
        - Focus on key takeaways and future outlook
        
        Generate appropriate content for this slide type.
        Keep it concise, engaging, and within the limits above.
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


def filesystem_writer_node(state: AgentState) -> dict[str, Any]:
    """Write the slide deck to filesystem."""
    if not state.deck:
        return {"error": "No deck available for writing"}

    writer = FilesystemWriter()

    # Determine output directory from metadata or use default
    output_dir = state.metadata.get("output_dir")

    try:
        # Write deck synchronously for now
        result = writer.write_deck_sync(state.deck, output_dir)

        return {
            "metadata": {
                **state.metadata,
                "filesystem_result": result,
                "slides_written": True,
                "output_path": result["output_path"],
            }
        }
    except Exception as e:
        return {"error": f"Failed to write slides: {str(e)}"}


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
    workflow.add_node("filesystem_writer", filesystem_writer_node)

    # Define the flow
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "slide_writer")
    workflow.add_edge("slide_writer", "reviewer")
    workflow.add_edge("reviewer", "filesystem_writer")
    workflow.add_edge("filesystem_writer", END)

    return workflow.compile()


def run_agent(topic_request: TopicRequest, output_dir: str = None) -> AgentState:
    """Run the slide generation agent workflow."""
    graph = create_agent_graph()

    initial_state = AgentState(
        request=topic_request,
        metadata={
            "session_id": "simple-run",
            "output_dir": output_dir,
        }
    )

    result = graph.invoke(initial_state)

    # Convert the result dict back to AgentState
    return AgentState(
        request=result.get("request", topic_request),
        outline=result.get("outline"),
        slides=result.get("slides"),
        deck=result.get("deck"),
        error=result.get("error"),
        metadata=result.get("metadata", {}),
    )
