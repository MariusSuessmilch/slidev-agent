"""Filesystem writer for slide decks."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles

from slide_agent.generators import SlideGenerator
from slide_agent.models import SlideDeck


class FilesystemWriter:
    """Writes slide decks to the filesystem in Slidev format."""

    def __init__(self, base_output_dir: str = "slides"):
        """Initialize filesystem writer."""
        self.base_output_dir = Path(base_output_dir)
        self.slide_generator = SlideGenerator()

    @staticmethod
    def create_slug(title: str) -> str:
        """Create URL-friendly slug from title."""
        # Remove special characters and convert to lowercase
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        # Replace spaces and multiple hyphens with single hyphen
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")[:50]  # Limit length

    def get_output_path(self, deck: SlideDeck, output_dir: str | None = None) -> Path:
        """Get the output directory path for a deck."""
        if output_dir:
            return Path(output_dir)

        slug = self.create_slug(deck.title)
        return self.base_output_dir / slug

    async def write_deck(
        self,
        deck: SlideDeck,
        output_dir: str | None = None,
        create_assets_dir: bool = True,
    ) -> dict[str, Any]:
        """Write slide deck to filesystem."""
        output_path = self.get_output_path(deck, output_dir)

        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)

        # Create assets directory
        if create_assets_dir:
            assets_dir = output_path / "assets"
            assets_dir.mkdir(exist_ok=True)

        # Generate markdown content
        markdown_content = self.slide_generator.generate_deck_markdown(deck)

        # Write main slides file
        slides_file = output_path / "slides.md"
        async with aiofiles.open(slides_file, "w", encoding="utf-8") as f:
            await f.write(markdown_content)

        # Write metadata file
        metadata = self._create_metadata(deck, output_path)
        meta_file = output_path / "meta.json"
        async with aiofiles.open(meta_file, "w", encoding="utf-8") as f:
            await f.write(json.dumps(metadata, indent=2, ensure_ascii=False))

        # Write package.json for Slidev
        package_json = self._create_package_json(deck)
        package_file = output_path / "package.json"
        async with aiofiles.open(package_file, "w", encoding="utf-8") as f:
            await f.write(json.dumps(package_json, indent=2))

        return {
            "output_path": str(output_path),
            "slides_file": str(slides_file),
            "meta_file": str(meta_file),
            "package_file": str(package_file),
            "assets_dir": str(assets_dir) if create_assets_dir else None,
            "slide_count": len(deck.slides),
            "size_bytes": len(markdown_content.encode("utf-8")),
        }

    def _create_metadata(self, deck: SlideDeck, output_path: Path) -> dict[str, Any]:
        """Create metadata for the deck."""
        return {
            "title": deck.title,
            "subtitle": deck.subtitle,
            "author": deck.author,
            "theme": deck.theme,
            "slide_count": len(deck.slides),
            "generated_at": datetime.now().isoformat(),
            "generated_by": "slidev-agent",
            "output_path": str(output_path),
            "slides": [
                {
                    "title": slide.title,
                    "type": slide.slide_type.value,
                    "notes": slide.notes,
                    "layout": slide.layout,
                    "transition": slide.transition,
                }
                for slide in deck.slides
            ],
            "fonts": deck.fonts,
            "css": deck.css,
            "metadata": deck.metadata,
        }

    def _create_package_json(self, deck: SlideDeck) -> dict[str, Any]:
        """Create package.json for Slidev project."""
        slug = self.create_slug(deck.title)

        return {
            "name": f"slidev-{slug}",
            "type": "module",
            "private": True,
            "scripts": {
                "build": "slidev build",
                "dev": "slidev --open",
                "export": "slidev export",
            },
            "dependencies": {
                "@slidev/cli": "^51.8.1",
                "@slidev/theme-default": "latest",
                f"slidev-theme-{deck.theme}": "latest",
                "vue": "^3.5.16",
            },
            "devDependencies": {"playwright-chromium": "^1.53.0"},
        }

    def write_deck_sync(
        self,
        deck: SlideDeck,
        output_dir: str | None = None,
        create_assets_dir: bool = True,
    ) -> dict[str, Any]:
        """Synchronous version of write_deck."""
        import asyncio

        return asyncio.run(self.write_deck(deck, output_dir, create_assets_dir))

    def create_readme(self, deck: SlideDeck, output_path: Path) -> str:
        """Create README.md for the slide deck."""
        slug = self.create_slug(deck.title)

        readme_content = f"""# {deck.title}

{deck.subtitle or "A presentation generated by Slidev Agent"}

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Export to PDF
npm run export
```

## Slides

This presentation contains {len(deck.slides)} slides:

{chr(10).join(f"{i+1}. {slide.title} ({slide.slide_type.value})" for i, slide in enumerate(deck.slides))}

## Theme

- **Theme**: {deck.theme}
- **Fonts**: {deck.fonts or 'Default'}

## Generated

- **Generated by**: Slidev Agent
- **Generated at**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Topic**: {deck.metadata.get('topic', 'Unknown')}

## Files

- `slides.md` - Main slide content
- `package.json` - Node.js dependencies
- `meta.json` - Slide metadata
- `assets/` - Images and other assets
"""

        return readme_content
