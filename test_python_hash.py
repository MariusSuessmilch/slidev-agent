#!/usr/bin/env python3
"""Test specifically for the python# case that's still occurring."""

from slide_agent.generators.slide_generator import SlideGenerator


def test_python_hash_fix():
    """Test the specific python# case that's causing issues."""

    # The exact case from the error
    input_text = "```python# Syntax of a simple decorator\ndef my_decorator(func):"
    expected = "```python\n# Syntax of a simple decorator\ndef my_decorator(func):"

    result = SlideGenerator._clean_code_blocks(input_text)

    print("Testing python# case specifically:")
    print(f"Input:    {repr(input_text)}")
    print(f"Expected: {repr(expected)}")
    print(f"Got:      {repr(result)}")
    print(f"Match:    {result == expected}")

    return result == expected


if __name__ == "__main__":
    success = test_python_hash_fix()
    if success:
        print("\n✅ python# case is handled correctly")
    else:
        print("\n❌ python# case is NOT handled - need to fix the regex")
