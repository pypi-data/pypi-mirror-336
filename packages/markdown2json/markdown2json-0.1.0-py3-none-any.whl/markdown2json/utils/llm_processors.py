"""
markdown2json.utils.llm_processors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Utility functions for processing markdown content using various LLM providers.
This module handles the integration with different LLM services and provides
standardized prompts for document analysis.

Key Features:
    - Multiple LLM provider support (Claude, OpenAI, Ollama)
    - Standardized prompt templates
    - Error handling and response processing
    - Specialized prompts for different document types

Example:
    >>> from markdown2json.utils.llm_processors import process_with_claude
    >>> result = await process_with_claude("Analyze this document...")
"""

import os
from typing import Dict, Any
from anthropic import AsyncAnthropic
from ollama import AsyncClient
import openai
import logging
import dotenv

# Load environment variables
dotenv.load_dotenv(override=True)

# Configure logging
logger = logging.getLogger(__name__)

# Constants
MAX_TOKENS = int(os.getenv("MARKDOWN2JSON_MAX_TOKENS", "4096"))
TIMEOUT = int(os.getenv("MARKDOWN2JSON_TIMEOUT", "30"))
DEFAULT_PROVIDER = os.getenv("MARKDOWN2JSON_LLM_PROVIDER", "CLAUDE")


async def process_with_claude(
    prompt: str, model: str = "claude-3-5-sonnet-20241022"
) -> Dict[str, Any]:
    """
    Process content using Anthropic's Claude model.

    This function sends the provided prompt to Claude and processes
    the response into a structured format.

    Args:
        prompt (str): The prompt to send to Claude

    Returns:
        str: Raw response from Claude

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set

    Example:
        >>> result = await process_with_claude("Analyze this table...")
        >>> print(result)
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    try:
        client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = await client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        # Handle response
        if hasattr(message, "content"):
            # Extract just the content text from the response
            content = message.content[0].text
            return content
        else:
            raise ValueError("Invalid response format from Claude API")

    except Exception as e:
        logger.error(f"Error processing with Claude: {str(e)}")
        raise


async def process_with_openai(prompt: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """
    Process content using OpenAI's GPT models.

    This function sends the provided prompt to OpenAI and processes
    the response into a structured format.

    Args:
        prompt (str): The prompt to send to OpenAI

    Returns:
        str: Raw response from OpenAI

    Raises:
        ValueError: If OPENAI_API_KEY is not set
        openai.OpenAIError: If the API request fails

    Example:
        >>> result = await process_with_openai("Extract data from...")
        >>> print(result)
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    try:
        client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = await client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error processing with OpenAI: {str(e)}")
        raise


async def process_with_ollama(prompt: str, model: str = "llama3.1") -> Dict[str, Any]:
    """
    Process content using local Ollama models.

    This function sends the provided prompt to a local Ollama instance
    and processes the response into a structured format.

    Args:
        prompt (str): The prompt to send to Ollama
        model (str): The Ollama model to use, defaults to "llama-3.1"

    Returns:
        Dict[str, Any]: Processed response from Ollama

    Raises:
        Exception: If the API request fails
    """
    if not os.getenv("OLLAMA_BASE_URL"):
        raise ValueError("OLLAMA_BASE_URL environment variable not set")
    try:
        client = AsyncClient(host=os.getenv("OLLAMA_BASE_URL"))
        message = {"role": "user", "content": prompt}
        response = await client.chat(model=model, messages=[message])
        return response.message.content
    except Exception as e:
        logger.error(f"Error processing with Ollama: {str(e)}")
        raise


def get_default_prompt(components: Dict[str, Any]) -> str:
    """
    Get default prompt for general document analysis.

    This function generates a standardized prompt for analyzing
    markdown content and converting it to structured JSON.

    Args:
        components (Dict[str, Any]): Document components to analyze

    Returns:
        str: Formatted prompt string

    Example:
        >>> prompt = get_default_prompt(document_components)
        >>> result = await process_with_claude(prompt)
    """
    return f"""
    You are an AI assistant specialized in converting markdown content to structured JSON.
    Analyze the provided markdown content and convert it into a well-structured JSON format.

    Guidelines:
    1. PRESERVE ALL CONTENT - Do not skip or omit any information
    2. Organize content into logical sections
    3. Preserve all numerical values and dates in their original format
    4. Convert tables into arrays of objects
    5. Maintain hierarchical relationships in the content
    6. Include any media URLs or links
    7. Ensure the output is valid JSON
    8. If content doesn't fit into a clear category, include it in a 'miscellaneous' or appropriate custom field
    
    Content:
    {components}

    Return only the JSON object, no additional text or explanation. Start your response with ```json and end with ```.
    """
