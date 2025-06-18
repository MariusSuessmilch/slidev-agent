"""CLI Interface for Slidev Agent."""

from typing import Optional

import typer
from rich.console import Console
from rich.traceback import install

from slide_agent.agent_graph import run_agent
from slide_agent.models import TopicRequest

# Install rich traceback handler
install()

console = Console()
app = typer.Typer()


@app.command()  # type: ignore[misc]
def main(
    topic: str = typer.Argument(..., help="Topic for slide generation"),
    audience: str = typer.Option("general", help="Target audience"),
    language: str = typer.Option("en", help="Language for the presentation"),
    slide_count: int = typer.Option(10, help="Number of slides to generate"),
    theme: str = typer.Option("the-unnamed", help="Slidev theme to use"),
    additional_context: Optional[str] = typer.Option(None, help="Additional context"),
    output_dir: str = typer.Option("slides", help="Output directory"),
) -> None:
    """Generate slides for a given topic using AI agents."""
    console.print(f"🚀 Generating slides for topic: [bold blue]{topic}[/bold blue]")
    console.print(
        f"📊 Settings: {slide_count} slides, {audience} audience, {language} language"
    )

    try:
        # Create topic request
        request = TopicRequest(
            topic=topic,
            audience=audience,
            language=language,
            slide_count=slide_count,
            theme=theme,
            additional_context=additional_context,
        )

        # Run the agent workflow
        console.print("🤖 Running agent workflow...")
        with console.status("[bold green]Processing..."):
            result = run_agent(request)

        # Display results
        if result.error:
            console.print(f"❌ Error: {result.error}")
            raise typer.Exit(1)

        if result.deck:
            console.print(
                f"✅ Generated deck: [bold green]{result.deck.title}[/bold green]"
            )
            console.print(f"📄 Slides created: {len(result.deck.slides)}")

            # Show slide titles
            console.print("\n📋 Slide titles:")
            for i, slide in enumerate(result.deck.slides, 1):
                console.print(f"  {i}. {slide.title} ({slide.slide_type.value})")

            # Show metadata if available
            if result.metadata:
                console.print(
                    f"\n🔍 Session: {result.metadata.get('session_id', 'unknown')}"
                )
        else:
            console.print("⚠️  No deck generated")

        console.print(f"\n💾 Output directory: {output_dir} (implementation in M3)")

    except Exception as e:
        console.print(f"❌ Failed to generate slides: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
