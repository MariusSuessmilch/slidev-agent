"""CLI Interface for Slidev Agent."""


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
    language: str = typer.Option("de", help="Language for the presentation"),
    slide_count: int = typer.Option(10, help="Number of slides to generate"),
    theme: str = typer.Option("the-unnamed", help="Slidev theme to use"),
    additional_context: str | None = typer.Option(None, help="Additional context"),
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
            result = run_agent(request, output_dir)

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

                # Show filesystem results
                if result.metadata.get("slides_written"):
                    output_path = result.metadata.get("output_path")
                    console.print(f"📁 Files written to: [bold green]{output_path}[/bold green]")

                    fs_result = result.metadata.get("filesystem_result", {})
                    console.print(f"📄 Main file: {fs_result.get('slides_file', 'index.md')}")
                    console.print(f"📊 Metadata: {fs_result.get('meta_file', 'meta.json')}")
                    console.print(f"📦 Package: {fs_result.get('package_file', 'package.json')}")

                    size_kb = fs_result.get("size_bytes", 0) / 1024
                    console.print(f"💾 Size: {size_kb:.1f} KB")
        else:
            console.print("⚠️  No deck generated")

        if not result.metadata.get("slides_written"):
            console.print(f"\n💾 Output directory: {output_dir} (no files written due to error)")

    except Exception as e:
        console.print(f"❌ Failed to generate slides: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
