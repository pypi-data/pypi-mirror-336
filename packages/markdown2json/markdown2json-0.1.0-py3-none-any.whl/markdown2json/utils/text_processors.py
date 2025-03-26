"""Text processing utilities"""

import re


def clean_text(text: str) -> str:
    """Clean text content by removing extra whitespace and newlines."""
    return re.sub(r"\s+", " ", text).strip()
