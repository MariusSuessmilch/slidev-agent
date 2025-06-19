#!/usr/bin/env python3
"""Test the full slide generation pipeline for code blocks."""

from slide_agent.generators.slide_generator import SlideGenerator
from slide_agent.models import SlideSpec, SlideType

def test_full_slide_generation():
    """Test generating a code slide with malformed content."""
    
    generator = SlideGenerator()
    
    # Create a slide with the problematic content
    slide = SlideSpec(
        title="Test Code Slide",
        slide_type=SlideType.CODE,
        content="```python# This is a comment\ndef my_function():\n    pass\n```",
        notes="Test slide"
    )
    
    print("Original slide content:")
    print(repr(slide.content))
    print()
    
    # Test the code extraction directly
    extracted = generator._extract_code_data(slide.content)
    print("Extracted code data:")
    print(f"  Language: {repr(extracted['language'])}")
    print(f"  Code: {repr(extracted['code'])}")
    print()
    
    # Generate the slide markdown
    result = generator.generate_slide(slide)
    
    print("Generated slide markdown:")
    print(result)
    print()
    
    # Check if malformed syntax exists in the result
    if "python#" in result:
        print("❌ FAILURE: Still contains python# in generated output")
        return False
    else:
        print("✅ SUCCESS: No python# found in generated output")
        return True

if __name__ == "__main__":
    test_full_slide_generation()