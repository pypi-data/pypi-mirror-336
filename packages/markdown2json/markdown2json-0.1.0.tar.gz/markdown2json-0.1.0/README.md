# markdown2json

A Python package for converting markdown content to structured JSON with advanced parsing capabilities and optional LLM-powered analysis.

## Features

- **Document Structure Analysis**
  - Convert markdown documents to structured JSON format
  - Preserve document hierarchy and section relationships
  - Extract metadata and document components
  
- **Table Processing**
  - Extract and analyze tables with context awareness
  - Determine table relationships and semantic roles
  - Generate table summaries and statistics
  
- **Advanced Analysis**
  - LLM integration with multiple providers (Claude, OpenAI, Ollama)
  - Semantic role detection for document elements
  - Context-aware content processing
  
- **Utility Features**
  - Batch processing for multiple documents
  - Customizable output formats
  - Rich metadata extraction

## Installation

```bash
# Basic installation
pip install markdown2json
```

## Requirements

- Python 3.8+
- Core Dependencies:
  - markdown>=3.3.0
  - beautifulsoup4>=4.9.0
  - markdown-it-py==3.0.0
  - python-dotenv==1.0.1
  
- Optional Dependencies:
  - anthropic>=0.3.0 (for Claude integration)
  - openai>=1.0.0 (for OpenAI integration)
  - ollama>=0.4.7 (for Ollama integration)

## Quick Start

```python
from markdown2json import MarkdownToJSON

# Initialize parser with markdown content
with open(PATH_TO_MARKDOWN_FILE, 'r', encoding='utf-8') as f:
    content = f.read()
parser = MarkdownToJSON(content)

# Extract all content including tables and structure
all_content = parser.extract_all_content()

# Extract only tables with context
tables = parser.extract_tables_by_page()

# Get table statistics
summary = parser.get_table_summary()
```

## Advanced Usage

### Table Extraction and Analysis

```python
from markdown2json import MarkdownToJSON
from pathlib import Path
import json

# Initialize parser
with open(PATH_TO_MARKDOWN_FILE, 'r', encoding='utf-8') as f:
    content = f.read()
parser = MarkdownToJSON(content)

# Extract tables with context
tables_by_page = parser.extract_tables_by_page()

# Get table summary
summary = parser.get_table_summary()
print(f"Total tables: {summary['total_tables']}")
print(f"Largest table: {summary['largest_table']}")

# Save output
output_dir = Path("output/table_analysis")
output_dir.mkdir(parents=True, exist_ok=True)

# Save table data as JSON
with open(output_dir / "tables_by_page.json", 'w', encoding='utf-8') as f:
    json.dump(tables_by_page, f, indent=2)
```

### LLM-Powered Analysis

```python
import asyncio
from markdown2json import MarkdownToJSON
from markdown2json.models.enums import LLMProvider
from markdown2json.utils import llm_processors

with open(PATH_TO_MARKDOWN_FILE, "r", encoding="utf-8") as f:
    content = f.read()

async def process_with_llm(markdown_content: str):
    # Initialize parser
    parser = MarkdownToJSON(markdown_content)
    
    # Get default prompt for content analysis
    prompt = llm_processors.get_default_prompt({
        "markdown_content": markdown_content
    })
    
    # Process with different LLM providers
    openai_result = await parser.process_with_llm(
        provider=LLMProvider.OPENAI,
        model=model_name, # gpt-4o, gpt-4o-mini, gpt-4-turbo
        custom_prompt=prompt
    )
    return openai_result

# Run async processing
result = asyncio.run(process_with_llm(content))
print(result)
```

### Batch Processing

```python
import asyncio
from pathlib import Path
from markdown2json import MarkdownToJSON
import json


async def process_files(input_dir: Path, output_dir: Path):
    # Validate input directory
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory {input_dir} does not exist")
    
    # Check for markdown files
    md_files = list(input_dir.glob("*.md"))
    if not md_files:
        raise ValueError(f"No markdown files found in {input_dir}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Processing files in {input_dir}")
    
    for md_file in md_files:
        try:
            print(f"Processing file: {md_file}")

            # Read markdown content
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Initialize parser
            parser = MarkdownToJSON(content)

            # Extract content
            tables = parser.extract_tables_by_page()
            summary = parser.get_table_summary()

            # Save outputs
            tables_output = output_dir / f"{md_file.stem}_tables.json"
            summary_output = output_dir / f"{md_file.stem}_summary.json"

            with open(tables_output, "w", encoding="utf-8") as f:
                json.dump(tables, f, indent=2)
            with open(summary_output, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)

        except Exception as e:
            print(f"Error processing {md_file}: {e}")

# Run batch processing
asyncio.run(process_files(Path("inputs"), Path("output")))
```

### Markdown to AST(Abstract Syntax Tree)

```python
# Import the MarkdownToJSON parser class
from markdown2json.parser import MarkdownToJSON
import json


def read_markdown_file(filename: str) -> str:
    """Read markdown from a file."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


# Read the markdown content from input file
markdown_content = read_markdown_file(PATH_TO_MARKDOWN_FILE)

# Initialize parser with markdown content
m2j = MarkdownToJSON(markdown_content)

# Convert markdown to Abstract Syntax Tree (AST) JSON format
# This creates a structured JSON representation of the markdown
json_content = m2j.markdown_to_ast()

# Print the JSON AST structure
print(json.dumps(json_content, indent=2))

# Convert the JSON AST back to markdown format
# This demonstrates roundtrip conversion from markdown -> JSON -> markdown
markdown_content = m2j.ast_to_markdown(json_content)

# Print the regenerated markdown
print(markdown_content)
```



## API Reference

### MarkdownToJSON Class

#### Core Methods

- `extract_document_components()`: Extract key document components including headers, footers, tables, and metadata
- `extract_tables_by_page()`: Extract tables organized by page with context
- `get_table_summary()`: Get statistical analysis of tables
- `extract_all_content()`: Get comprehensive document analysis
- `json_to_markdown()`: Convert JSON structure back to markdown
- `markdown_to_ast()`: Converts the markdown to the json format in AST(Abstract Syntax Tree) Approach.
- `ast_to_markdown()`: Revert back the json format to the markdown( Note : the json format should follow AST aproach to revert back.)

#### LLM Integration

- `process_with_llm()`: Process content with LLM providers
  - Supports Claude, OpenAI, and Ollama
  - Customizable prompts
  - Async processing

## Project Structure

```
markdown2json/
├── parser.py          # Main parser implementation
├── models/            # Data models and enums
├── utils/            
│   ├── text_processors.py    # Text processing utilities
│   ├── extractors.py        # Content extraction tools
│   └── llm_processors.py    # LLM integration
└── helpers/
    └── document_analyzer.py  # Document analysis tools
```

## Configuration

The package behavior can be customized through environment variables:

- `MARKDOWN2JSON_LLM_PROVIDER`: Default LLM provider
- `MARKDOWN2JSON_MAX_TOKENS`: Maximum tokens for LLM requests
- `MARKDOWN2JSON_TIMEOUT`: Request timeout in seconds

## Troubleshooting

Common issues and solutions:

1. **Table Extraction Issues**
   - Ensure tables are properly formatted in markdown
   - Check for missing headers or malformed cells

2. **LLM Integration**
   - Verify API keys are properly set
   - Check network connectivity
   - Ensure proper provider configuration

3. **Performance Issues**
   - Consider batch processing for large files
   - Use appropriate chunk sizes for LLM requests

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License

## Support

For support:
- Open an issue on GitHub
- Check the [documentation](https://markdown2json.readthedocs.io)
- Contact maintainers at support@markdown2json.com

## Changelog

### Version 0.1.0
- Initial release
- Basic markdown to JSON conversion
- Table extraction and analysis
- LLM integration
- Document component extraction
