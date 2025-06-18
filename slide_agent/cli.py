"""CLI Interface for Slidev Agent."""

import typer
from rich.console import Console

console = Console()
app = typer.Typer()


@app.command()  # type: ignore[misc]
def main(topic: str = typer.Argument(..., help="Topic for slide generation")) -> None:
    """Generate slides for a given topic."""
    console.print(f"🚀 Generating slides for topic: [bold blue]{topic}[/bold blue]")
    console.print("⚠️  Implementation coming in M3...")


if __name__ == "__main__":
    app()
