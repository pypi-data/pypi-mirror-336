import unittest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from markdown2json.parser import MarkdownToJSON
from markdown2json.utils import llm_processors
from markdown2json.models.enums import LLMProvider


class TestLLMExtractor(unittest.TestCase):
    def setUp(self):
        self.sample_markdown = """# Project Report
## Overview
Project Name: PROJ-001
Start Date: 2024-01-01

## Tasks
| Task | Hours | Status |
|------|-------|--------|
| Task1 | 8 | Complete |
| Task2 | 4 | Pending |
"""
        self.parser = MarkdownToJSON(self.sample_markdown)

        self.sample_json_content = {
            "project_details": {"name": "PROJ-001", "start_date": "2024-01-01"},
            "tasks": [
                {"task": "Task1", "hours": 8, "status": "Complete"},
                {"task": "Task2", "hours": 4, "status": "Pending"},
            ],
        }

    def test_llm_processor_functions(self):
        test_data = {
            "content": "Sample markdown content",
            "metadata": {"type": "document", "format": "markdown"},
        }

        # Test default prompt generation
        prompt = llm_processors.get_default_prompt(test_data)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def async_test(f):
        def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(f(*args, **kwargs))

        return wrapper

    @async_test
    async def test_process_with_llm(self):
        mock_response = MagicMock()
        mock_response.content = '{"header_info": {"company_info": "data"}}'

        with patch("anthropic.AsyncAnthropic") as mock_client:
            mock_client.return_value.messages.create = AsyncMock(
                return_value=mock_response
            )
            result = await self.parser.process_with_llm(provider=LLMProvider.CLAUDE)
            self.assertIsInstance(result, str)
            self.assertIn("header_info", result)

    @async_test
    async def test_process_with_llm_different_providers(self):
        # Mock responses for different providers
        claude_response = MagicMock()
        claude_response.content = '{"header_info": {"company_info": "data"}}'

        openai_response = MagicMock()
        openai_response.choices = [
            MagicMock(
                message=MagicMock(content='{"header_info": {"company_info": "data"}}')
            )
        ]

        # Test Claude
        with patch("anthropic.AsyncAnthropic") as mock_claude:
            mock_claude.return_value.messages.create = AsyncMock(
                return_value=claude_response
            )
            result = await self.parser.process_with_llm(provider=LLMProvider.CLAUDE)
            self.assertIsInstance(result, str)
            self.assertIn("header_info", result)

        # Test OpenAI
        with patch("openai.AsyncOpenAI") as mock_openai:
            mock_openai.return_value.chat.completions.create = AsyncMock(
                return_value=openai_response
            )
            result = await self.parser.process_with_llm(provider=LLMProvider.OPENAI)
            self.assertIsInstance(result, str)
            self.assertIn("header_info", result)

        # Test Ollama
        with self.assertRaises(NotImplementedError):
            await self.parser.process_with_llm(provider=LLMProvider.OLLAMA)

    @async_test
    async def test_process_with_llm_error_handling(self):
        # Test missing API key
        with patch.dict("os.environ", clear=True):
            with self.assertRaises(ValueError):
                await self.parser.process_with_llm(provider=LLMProvider.CLAUDE)

        # Test API error
        with patch("anthropic.AsyncAnthropic") as mock_client:
            mock_client.return_value.messages.create = AsyncMock(
                side_effect=Exception("API Error")
            )
            result = await self.parser.process_with_llm(
                provider=LLMProvider.CLAUDE, model="claude-invalid-model"
            )
            self.assertIsInstance(result, dict)
            self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
