"""
markdown2json - A Python package for converting markdown to structured JSON
"""

from markdown2json.parser import MarkdownToJSON
from markdown2json.models.enums import LLMProvider

__version__ = "0.1.0"
__all__ = ["MarkdownToJSON", "LLMProvider"]
