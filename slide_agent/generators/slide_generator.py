"""Slide generation using Jinja templates."""

import os
import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from slide_agent.models import SlideDeck, SlideSpec, SlideType


class SlideGenerator:
    """Generates Slidev markdown from slide specifications."""

    def __init__(self, templates_dir: Path | None = None):
        """Initialize the slide generator with Jinja environment."""
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates"

        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=False,
            lstrip_blocks=False,
        )

        # Register custom filters
        self.env.filters["slugify"] = self.slugify

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-friendly slug."""
        # Remove special characters and convert to lowercase
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        # Replace spaces and multiple hyphens with single hyphen
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")

    @staticmethod
    def _clean_code_blocks(content: str) -> str:
        """Clean up malformed code blocks."""
        if not content:
            return content

        # Fix malformed code blocks where language is concatenated with code
        # Use a single comprehensive regex that matches the most common patterns
        # Order by length (longest first) to avoid partial matches

        # Define all valid languages in order of specificity
        languages = [
            "javascript",
            "typescript",
            "python",
            "html",
            "bash",
            "yaml",
            "json",
            "java",
            "cpp",
            "css",
            "sql",
            "xml",
            "c",
        ]

        # Create pattern that matches any language followed by a letter/underscore/special chars
        # But NOT followed by newline (which indicates properly formatted code)
        pattern = r"```(" + "|".join(languages) + r")(?=[a-zA-Z_<.{[#-])"

        def replace_match(match):
            lang = match.group(1)
            return f"```{lang}\n"

        content = re.sub(pattern, replace_match, content)

        return content

    @staticmethod
    def _clean_duplicate_titles(content: str, slide_title: str) -> str:
        """Remove duplicate title lines from LLM responses."""
        if not content or not slide_title:
            return content

        lines = content.split("\n")
        cleaned_lines = []

        for line in lines:
            line_stripped = line.strip()
            # Skip lines that are duplicate titles in various formats
            if (
                line_stripped.lower() == f"title: {slide_title.lower()}"
                or line_stripped.lower() == slide_title.lower()
                or line_stripped.lower() == f"# {slide_title.lower()}"
                or line_stripped == f"# {slide_title}"
                or line_stripped.lower().startswith(f"# {slide_title.lower()}")
                or line_stripped.startswith(f"# {slide_title}")
            ):
                continue
            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    @staticmethod
    def _limit_slide_lines(content: str, max_lines: int = 10) -> str:
        """Ensure slide content doesn't exceed maximum line count."""
        if not content:
            return content

        lines = content.split("\n")
        # Count non-empty lines for the limit
        non_empty_lines = [line for line in lines if line.strip()]

        if len(non_empty_lines) <= max_lines:
            return content

        # If we have too many lines, keep the most important ones
        # Keep first few lines and last line if it's a conclusion
        keep_lines = non_empty_lines[: max_lines - 1]
        last_line = non_empty_lines[-1]

        # Add the last line if it seems like a conclusion or call-to-action
        if any(
            word in last_line.lower()
            for word in ["zusammenfassung", "fazit", "ausblick", "zukunft", "wichtig"]
        ):
            keep_lines.append(last_line)
        else:
            keep_lines.append(non_empty_lines[max_lines - 1])

        return "\n".join(keep_lines[:max_lines])

    def generate_frontmatter(self, deck: SlideDeck) -> str:
        """Generate the Slidev frontmatter."""
        template = self.env.get_template("deck_frontmatter.md.j2")

        # Prepare frontmatter data
        data = {
            "theme": deck.theme,
            "title": deck.title,
            "info": deck.subtitle or f"## {deck.title}",
            "css_class": "text-center",
            "transition": "slide-left",
            "fonts": deck.fonts or {"sans": "Montserrat"},
        }

        return template.render(**data)

    def generate_slide(self, slide: SlideSpec, is_first: bool = False) -> str:
        """Generate a single slide from specification."""
        # Clean up malformed code blocks in content
        slide.content = self._clean_code_blocks(slide.content)

        # Clean up duplicate title lines from LLM responses
        slide.content = self._clean_duplicate_titles(slide.content, slide.title)

        # Ensure content doesn't exceed line limits
        slide.content = self._limit_slide_lines(slide.content, max_lines=10)

        # Determine template based on slide type
        template_map = {
            SlideType.TITLE: "title_slide.md.j2",
            SlideType.BULLETS: "bullets_slide.md.j2",
            SlideType.CODE: "code_slide.md.j2",
            SlideType.COMPARISON: "comparison_slide.md.j2",
            SlideType.QUOTE: "quote_slide.md.j2",
            SlideType.DIAGRAM: "bullets_slide.md.j2",  # Fallback for now
            SlideType.IMAGE: "bullets_slide.md.j2",  # Fallback for now
        }

        template_name = template_map.get(slide.slide_type, "bullets_slide.md.j2")
        template = self.env.get_template(template_name)

        # Prepare slide data
        data = self._prepare_slide_data(slide, is_first)

        # Optional debug output for code slides (can be enabled via environment variable)
        if os.getenv("SLIDEV_DEBUG") and slide.slide_type == SlideType.CODE:
            print("DEBUG - Template data for code slide:")
            print(f"  Template: {template_name}")
            print(f"  Language: {data.get('language', 'NOT_SET')}")
            print(f"  Code: {repr(data.get('code', 'NOT_SET'))}")
            print(f"  Content: {repr(data.get('content', 'NOT_SET'))}")

        return template.render(**data)

    def _prepare_slide_data(
        self, slide: SlideSpec, is_first: bool = False
    ) -> dict[str, Any]:
        """Prepare data for slide template rendering."""
        data = {
            "title": slide.title,
            "content": slide.content,
            "notes": slide.notes,
            "layout": slide.layout,
            "transition": slide.transition,
            "background": slide.background,
        }

        # Add type-specific data
        if slide.slide_type == SlideType.TITLE:
            data.update(
                {
                    "subtitle": None,  # Will use content as subtitle
                    "click_to_next": is_first,  # Only first slide gets click handler
                }
            )

        elif slide.slide_type == SlideType.CODE:
            data.update(self._extract_code_data(slide.content))

        elif slide.slide_type == SlideType.BULLETS:
            data.update(self._extract_bullets_data(slide.content))

        elif slide.slide_type == SlideType.COMPARISON:
            data.update(self._extract_comparison_data(slide.content))

        elif slide.slide_type == SlideType.QUOTE:
            data.update(self._extract_quote_data(slide.content))

        return data

    def _extract_code_data(self, content: str) -> dict[str, Any]:
        """Extract code, language, and explanation from content."""
        lines = content.split("\n")
        code_lines = []
        explanation_lines = []
        language = "python"  # Default
        in_code_block = False
        found_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                if not in_code_block:
                    # Start of code block
                    lang = line.strip()[3:].strip()
                    if lang:
                        # Clean up language name - remove any extra characters
                        language = lang.split()[0].lower()  # Take first word, lowercase
                        # Remove any non-alphanumeric characters (like # symbols)
                        language = "".join(c for c in language if c.isalnum())
                    in_code_block = True
                    found_code_block = True
                else:
                    # End of code block
                    in_code_block = False
                    # Stop processing after first code block to avoid duplicates
                    break
            elif in_code_block:
                code_lines.append(line)
            elif not found_code_block:
                # Only collect explanation lines before first code block
                explanation_lines.append(line)

        # Validate language name and remove any special characters
        valid_languages = [
            "python",
            "javascript",
            "typescript",
            "java",
            "cpp",
            "c",
            "sql",
            "bash",
            "html",
            "css",
            "json",
            "yaml",
            "xml",
        ]
        # Clean language name: keep only alphanumeric, convert to lowercase
        language = "".join(c for c in language if c.isalnum()).lower()

        # Handle common variations and ensure valid language
        language_mapping = {
            "js": "javascript",
            "ts": "typescript",
            "py": "python",
            "sh": "bash",
            "htm": "html",
        }
        language = language_mapping.get(language, language)

        if language not in valid_languages:
            language = "python"  # Default fallback

        return {
            "code": "\n".join(code_lines).strip(),
            "language": language,
            "explanation": "\n".join(explanation_lines).strip() or None,
            "highlight_lines": None,  # TODO: Extract from content
        }

    def _extract_bullets_data(self, content: str) -> dict[str, Any]:
        """Extract bullet points and check for two-column layout."""
        lines = content.split("\n")
        bullet_points = []
        text_content = []

        for line in lines:
            line = line.strip()
            # Only accept top-level bullets (no nested/indented bullets)
            if (line.startswith("- ") or line.startswith("* ")) and not line.startswith(
                "  "
            ):
                # Remove bullet marker and clean up
                bullet_text = line[2:].strip()
                # Remove any sub-bullet formatting that might remain
                if (
                    bullet_text
                    and not bullet_text.startswith("-")
                    and not bullet_text.startswith("*")
                ):
                    bullet_points.append(bullet_text)
            elif (
                line and not line.startswith("#") and not line.startswith("  ")
            ):  # Skip indented lines
                text_content.append(line)

        return {
            "bullet_points": bullet_points[:5]
            if bullet_points
            else None,  # Limit to 5 bullets
            "content": "\n".join(text_content).strip() if text_content else None,
            "two_column": False,  # TODO: Detect from content
            "left_content": None,
            "right_content": None,
        }

    def _extract_comparison_data(self, content: str) -> dict[str, Any]:
        """Extract left and right content for comparison slides."""
        # Simple split by "vs" or "compared to"
        parts = re.split(
            r"\s+(vs\.?|compared to|versus)\s+", content, flags=re.IGNORECASE
        )

        if len(parts) >= 3:
            left_content = parts[0].strip()
            right_content = parts[2].strip()
        else:
            # Fallback: split by half
            mid = len(content) // 2
            left_content = content[:mid].strip()
            right_content = content[mid:].strip()

        return {
            "left_title": "Option A",
            "left_content": left_content,
            "right_title": "Option B",
            "right_content": right_content,
        }

    def _extract_quote_data(self, content: str) -> dict[str, Any]:
        """Extract quote and author from content."""
        # First clean up any malformed code blocks
        content = self._clean_code_blocks(content)

        # Remove empty code blocks that might remain
        content = re.sub(r"```\s*\n\s*```", "", content)
        content = re.sub(r"```\s*```", "", content)

        lines = content.split("\n")
        quote_lines = []
        author = None

        for line in lines:
            line = line.strip()
            # Skip empty lines and code block markers
            if not line or line == "```":
                continue
            if line.startswith("—") or line.startswith("- "):
                author = line[1:].strip()
            elif line.startswith(">"):
                quote_lines.append(line[1:].strip())
            elif line:  # Only add non-empty lines
                quote_lines.append(line)

        quote_text = "\n".join(quote_lines).strip()

        return {
            "quote": quote_text if quote_text else None,
            "author": author,
            "additional_content": None,
        }

    def generate_deck_markdown(self, deck: SlideDeck) -> str:
        """Generate complete Slidev markdown for the deck."""
        parts = []

        # Add frontmatter
        parts.append(self.generate_frontmatter(deck))
        parts.append("")  # Empty line after frontmatter

        # Add slides
        for i, slide in enumerate(deck.slides):
            is_first = i == 0

            # Add slide content
            slide_content = self.generate_slide(slide, is_first)

            # Check if slide content already starts with frontmatter
            if i > 0 and not slide_content.strip().startswith("---"):
                # Add slide separator only if content doesn't have its own
                slide_separator_parts = ["---"]
                if slide.transition:
                    slide_separator_parts.append(f"transition: {slide.transition}")
                if slide.layout:
                    slide_separator_parts.append(f"layout: {slide.layout}")
                slide_separator_parts.append("---")
                parts.append("\n".join(slide_separator_parts))

            parts.append(slide_content)
            parts.append("")  # Empty line between slides

        return "\n".join(parts)
