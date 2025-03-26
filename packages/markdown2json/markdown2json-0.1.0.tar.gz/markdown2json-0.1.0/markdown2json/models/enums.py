"""Enums used throughout the package"""

from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers"""

    OPENAI = "openai"
    CLAUDE = "claude"
    OLLAMA = "ollama"
