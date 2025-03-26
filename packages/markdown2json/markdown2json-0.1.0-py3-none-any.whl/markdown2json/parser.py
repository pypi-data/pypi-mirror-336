"""
markdown2json.parser
~~~~~~~~~~~~~~~~~~

Main parser module for converting markdown content to structured JSON format.
Provides comprehensive document analysis, table extraction, and LLM integration
capabilities.

Key Features:
    - Document structure analysis and component extraction
    - Table detection and contextual analysis
    - LLM-powered content processing
    - Metadata extraction and organization

Example:
    >>> from markdown2json import MarkdownToJSON
    >>> parser = MarkdownToJSON(content)
    >>> components = parser.extract_document_components()
    >>> tables = parser.extract_tables_by_page()
"""

import markdown
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional, Union
from markdown_it import MarkdownIt
from markdown_it.token import Token
import re

from .models.enums import LLMProvider
from .utils import text_processors, extractors, llm_processors
from .helpers import document_analyzer


class MarkdownToJSON:
    """
    Main parser class for converting markdown content to structured JSON format.

    This class provides comprehensive functionality for:
    - Extracting document components and structure
    - Analyzing tables and their context
    - Processing content with LLM providers
    - Generating metadata and summaries

    Attributes:
        markdown_content (str): The original markdown content
        _html_content (str): Intermediate HTML representation
        _soup (BeautifulSoup): Parsed HTML structure
        _sections_stack (List): Track section nesting
        _section_path (List[str]): Current section hierarchy path
    """

    def __init__(self, markdown_content: str):
        """
        Initialize the converter with markdown content.

        Args:
            markdown_content (str): The markdown content to be converted

        Raises:
            TypeError: If markdown_content is None or not a string
            ValueError: If markdown_content is empty or contains only whitespace/
            special characters
        """
        if markdown_content is None:
            raise TypeError("Markdown content cannot be None")
        if not isinstance(markdown_content, str):
            raise TypeError("Markdown content must be a string")

        # Strip whitespace and check for empty content
        cleaned_content = markdown_content.strip()
        if not cleaned_content:
            raise ValueError("Markdown content cannot be empty")

        # Check if content only contains special characters or whitespace
        if not any(c.isalnum() for c in cleaned_content):
            raise ValueError(
                "Markdown content must contain at least one alphanumeric character"
            )

        self.markdown_content = markdown_content
        self._html_content = markdown.markdown(
            markdown_content,
            extensions=[
                "tables",
                "fenced_code",
                "nl2br",
                "def_list",
                "footnotes",
                "attr_list",
                "md_in_html",
                "smarty",
                "codehilite",
            ],
        )

        # Validate HTML content after conversion
        if not self._html_content.strip():
            raise ValueError(
                "Failed to convert markdown to HTML - resulting HTML is empty"
            )

        self._soup = BeautifulSoup(self._html_content, "html.parser")

        # Validate parsed content
        if not list(self._soup.children):
            raise ValueError(
                "Failed to parse markdown content - no valid content found"
            )

        self._sections_stack = []
        self._section_path = []

    def extract_document_components(self) -> Dict[str, Any]:
        """
        Extract and organize key components from the markdown document.

        This method provides a comprehensive analysis of the document structure,
        extracting various components and their relationships.

        Returns:
            Dict containing:
            - header_info: Document header information and metadata
            - footer_info: Document footer content and references
            - tables: List of tables with their context and structure
            - metadata: Document metadata including hierarchy
            - misc_details: Additional document elements and details

        Example:
            >>> parser = MarkdownToJSON(content)
            >>> components = parser.extract_document_components()
            >>> print(components['header_info'])
        """
        parsed_content = self.parse()

        components = {
            "header_info": document_analyzer.extract_header_info(parsed_content),
            "footer_info": document_analyzer.extract_footer_info(parsed_content),
            "lists": self._extract_lists(parsed_content),
            "tables": self._extract_tables(parsed_content),
            "metadata": self._extract_metadata(parsed_content),
            "misc_details": self._extract_misc_details(parsed_content),
        }

        return components

    def _extract_tables(self, parsed_content: Dict) -> List[Dict]:
        """
        Extract and analyze tables from the document with context.

        Args:
            parsed_content (Dict): The parsed document structure

        Returns:
            List[Dict]: List of tables with their data, context, and location

        Each table dictionary contains:
        - data: The table content and structure
        - context: Surrounding text and semantic context
        - path: Location in document hierarchy
        """
        tables = []

        def process_content(content):
            for item in content:
                if item.get("type") == "table":
                    table_info = {
                        "data": item.get("data", {}),
                        "context": extractors.determine_table_context(item),
                        "path": item.get("path", []),
                    }
                    tables.append(table_info)
                elif "content" in item:
                    process_content(item["content"])

        process_content(parsed_content.get("content", []))
        return tables

    def _extract_lists(self, parsed_content: Dict) -> List[Dict]:
        """
        Extract and analyze lists from the document.

        Args:
            parsed_content (Dict): The parsed document structure

        Returns:
            List[Dict]: List of lists with their data and structure
        """
        lists = []

        def process_content(content):
            for item in content:
                if item.get("type") == "list":
                    lists.append(item)
                if "content" in item:
                    process_content(
                        item["content"]
                    )  # Recursively process nested content

        process_content(parsed_content.get("content", []))
        return lists

    def _extract_metadata(self, parsed_content: Dict) -> Dict:
        """
        Extract document metadata and structural information.

        Args:
            parsed_content (Dict): The parsed document structure

        Returns:
            Dict containing:
            - document_structure: Section hierarchy and relationships
            - links: Document links and references
            - images: Image information and captions
        """
        return {
            "document_structure": {
                "sections": self._get_document_sections(),
                "hierarchy": self._get_section_hierarchy(),
            },
            "links": extractors.extract_links(self._soup),
            "images": extractors.extract_images(self._soup),
        }

    def _extract_misc_details(self, parsed_content: Dict) -> Dict:
        """Extract miscellaneous details from the document."""
        misc_details = {
            "dates": [],
            "amounts": [],
            "reference_numbers": [],
            "contact_info": [],
        }

        def process_content(content):
            for item in content:
                if item.get("type") in ["text", "key_value"]:
                    role = item.get("semantic_role", "")
                    if role == "date":
                        misc_details["dates"].append(item)
                    elif role == "amount":
                        misc_details["amounts"].append(item)
                    elif "number" in item.get("text", "").lower():
                        misc_details["reference_numbers"].append(item)
                    elif any(
                        word in item.get("text", "").lower()
                        for word in ["phone", "email", "fax"]
                    ):
                        misc_details["contact_info"].append(item)

                if "content" in item:
                    process_content(item["content"])

        process_content(parsed_content.get("content", []))
        return misc_details

    def _get_document_sections(self) -> List[Dict]:
        """Get list of document sections with their levels and paths."""
        sections = []
        for element in self._soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            level = int(element.name[1])
            title = text_processors.clean_text(element.get_text())
            sections.append(
                {
                    "title": title,
                    "level": level,
                    "path": self._get_current_section_path() + [title],
                }
            )
        return sections

    def _get_section_hierarchy(self) -> Dict:
        """Get the hierarchical structure of document sections."""
        hierarchy = {}
        current_path = []

        for section in self._get_document_sections():
            level = section["level"]
            title = section["title"]

            # Adjust current path based on level
            while len(current_path) >= level:
                current_path.pop()
            current_path.append(title)

            # Build hierarchy path
            path_key = ".".join(current_path)
            parent_key = ".".join(current_path[:-1]) if current_path[:-1] else None

            hierarchy[path_key] = {"level": level, "parent": parent_key, "children": []}

            if parent_key and parent_key in hierarchy:
                hierarchy[parent_key]["children"].append(path_key)

        return hierarchy

    def parse(self) -> Dict:
        """
        Parse the markdown content into a structured dictionary.

        Returns:
            Dict containing parsed content with structure and metadata
        """
        content = []
        current_section = None

        for element in self._soup.children:

            if element.name:
                parsed = self._parse_element(element, current_section)
                if parsed:
                    for item in parsed:
                        if item.get("type") == "heading":
                            current_section = item.get("text", "").strip()
                            self._section_path.append(current_section)
                        item["path"] = self._section_path.copy()
                        content.append(item)

        return {
            "content": content,
            "metadata": self._extract_metadata({"content": content}),
            "document_info": {
                "total_sections": len(self._get_document_sections()),
                "has_header": bool(content and content[0].get("type") == "heading"),
                "has_footer": bool(
                    content and content[-1].get("type") in ["paragraph", "list"]
                ),
            },
        }

    def _parse_element(
        self, element, current_section: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """Parse individual HTML elements into structured data."""
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            return [self._parse_header(element)]
        elif element.name == "p":
            return self._parse_paragraph(element, current_section)
        elif element.name == "table":
            return [self._parse_table(element, current_section)]
        elif element.name in ["ul", "ol"]:
            return [self._parse_list(element, current_section)]
        elif element.name is not None:  # Handle other elements (e.g., div, span)
            # Recursively parse child elements and pass the current_section
            parsed_children = []
            for child in element.children:
                if hasattr(child, "name"):
                    parsed = self._parse_element(child, current_section)
                    if parsed:
                        parsed_children.extend(parsed)
            return parsed_children

        return None

    def _parse_header(self, element) -> Dict:
        """Parse header elements into structured data."""
        text = element.get_text().strip()
        level = int(element.name[1])  # h1 -> 1, h2 -> 2, etc.

        return {"type": "heading", "text": text, "level": level}

    def _parse_paragraph(
        self, element, current_section: Optional[str] = None
    ) -> List[Dict]:
        """Parse paragraph elements, detecting key-value pairs."""
        text = element.get_text().strip()
        results = []

        # Handle multi-line content
        lines = text.split("\n")

        for line in lines:
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Normalize tax key
                if key.startswith("Tax"):
                    key = "Tax"

                results.append(
                    {
                        "type": "key_value",
                        "key": key,
                        "value": value,
                        "section": current_section,
                        "semantic_role": self._determine_semantic_role(key, value),
                    }
                )

        if results:
            return results

        return [{"type": "text", "text": text, "section": current_section}]

    def _determine_semantic_role(self, key: str, value: str) -> str:
        """Determine the semantic role of a key-value pair."""
        key_lower = key.lower()
        if any(date_word in key_lower for date_word in ["date", "due"]):
            return "date"
        elif any(
            amount_word in key_lower
            for amount_word in ["total", "amount", "price", "tax", "subtotal"]
        ):
            return "amount"
        elif any(ref_word in key_lower for ref_word in ["number", "id", "reference"]):
            return "reference"
        return "general"

    def _parse_table(self, element, current_section: Optional[str] = None) -> Dict:
        """Parse table elements into structured data."""
        headers = []
        rows = []

        # Extract headers
        header_row = element.find("tr")
        if header_row:
            headers = [
                th.get_text().strip() for th in header_row.find_all(["th", "td"])
            ]

        # Extract rows
        for row in element.find_all("tr")[1:]:  # Skip header row
            cells = [td.get_text().strip() for td in row.find_all("td")]
            if len(cells) == len(headers):
                row_data = dict(zip(headers, cells))
                rows.append(row_data)

        return {
            "type": "table",
            "data": {"headers": headers, "rows": rows},
            "section": current_section,
        }

    def _parse_list(self, element, current_section: Optional[str] = None) -> Dict:
        """
        Parse list elements (unordered or ordered) into structured data.
        Handles:
        - Nested lists inside list items
        - Lists appearing directly inside another list (fixes missing initial nesting)
        """
        list_type = "ordered" if element.name == "ol" else "unordered"
        items = []

        for li in element.find_all("li", recursive=False):  # Only direct children <li>
            # Extract text content for the parent list item (excluding nested lists)
            parent_text = "".join(
                str(c) if isinstance(c, str) else c.get_text(strip=True)
                for c in li.contents
                if c.name not in ["ul", "ol"]  # Exclude nested lists from main text
            ).strip()

            # Initialize the list item data
            item_data = {"text": parent_text}

            # Process nested lists inside the current <li>
            nested_lists = li.find_all(
                ["ul", "ol"], recursive=False
            )  # Only immediate nested lists
            for nested_list in nested_lists:
                nested_list_data = self._parse_list(nested_list, current_section)
                if nested_list_data["items"]:  # Only add if it has content
                    item_data.setdefault("nested_lists", []).append(nested_list_data)

            items.append(item_data)

        # Fix for initial nested lists: if a list is inside another list but
        # not inside <li>
        nested_lists = element.find_all(
            ["ul", "ol"], recursive=False
        )  # Only immediate child lists
        for nested_list in nested_lists:
            if nested_list not in element.find_all("li"):
                nested_list_data = self._parse_list(nested_list, current_section)
                if nested_list_data["items"]:  # Only add if it has content
                    items.append(nested_list_data)

        return {
            "type": "list",
            "list_type": list_type,
            "items": items,
            "section": current_section,
        }

    def extract_tables_by_page(self) -> Dict[str, List[Dict]]:
        """
        Extract tables from the markdown document organized by page.
        If page information is not available, tables will be grouped under
        'unknown_page'.

        Returns:
            Dict with page numbers as keys and lists of tables as values.
            Each table includes:
            - headers: List of column headers
            - rows: List of rows with cell data
            - context: The context/purpose of the table
            - section: Section title where the table appears
            - preceding_text: Any text immediately before the table
        """
        tables_by_page = {}
        current_page = "unknown_page"

        def process_element(element, current_section=None):
            nonlocal current_page

            # Check for page markers
            if isinstance(element, str):
                page_match = re.search(r"page\s*(\d+)(?:/\d+)?", element.lower())
                if page_match:
                    current_page = f"page{page_match.group(1)}"
                    return

            # Initialize page in dict if not exists
            if current_page not in tables_by_page:
                tables_by_page[current_page] = []

            # Process table elements
            if element.name == "table":
                table_data = self._parse_table(element)

                # Get preceding text (if any)
                preceding_text = ""
                prev_sibling = element.find_previous_sibling()
                if prev_sibling and prev_sibling.name == "p":
                    preceding_text = text_processors.clean_text(prev_sibling.get_text())

                # Add additional context
                table_info = {
                    "headers": table_data["data"]["headers"],
                    "rows": table_data["data"]["rows"],
                    "context": extractors.determine_table_context(table_data),
                    "section": current_section,
                    "preceding_text": preceding_text,
                    "path": table_data.get("path", []),
                }

                tables_by_page[current_page].append(table_info)

            # Process child elements
            if hasattr(element, "children"):
                current_section_title = None
                if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                    current_section_title = text_processors.clean_text(
                        element.get_text()
                    )

                for child in element.children:
                    if isinstance(child, str):
                        process_element(child, current_section or current_section_title)
                    elif hasattr(child, "name"):
                        process_element(child, current_section or current_section_title)

        # Process the document
        for element in self._soup.children:
            process_element(element)

        # Clean up empty pages
        tables_by_page = {k: v for k, v in tables_by_page.items() if v}

        # Sort pages by number if possible
        try:
            sorted_pages = sorted(
                tables_by_page.items(),
                key=lambda x: (
                    int(x[0].replace("page", ""))
                    if x[0] != "unknown_page"
                    else float("inf")
                ),
            )
            tables_by_page = dict(sorted_pages)
        except Exception:
            pass

        return tables_by_page

    def get_table_summary(self) -> Dict:
        """
        Get a summary of all tables in the document.

        Returns:
            Dict containing:
            - total_tables: Total number of tables
            - tables_by_page: Count of tables per page
            - table_contexts: Types of tables found
            - largest_table: Info about the largest table
        """
        tables = self.extract_tables_by_page()

        summary = {
            "total_tables": 0,
            "tables_by_page": {},
            "table_contexts": set(),
            "largest_table": {"rows": 0, "columns": 0, "page": None, "context": None},
        }

        for page, page_tables in tables.items():
            summary["tables_by_page"][page] = len(page_tables)
            summary["total_tables"] += len(page_tables)

            for table in page_tables:
                # Track contexts
                if "context" in table:
                    summary["table_contexts"].add(table["context"])

                # Track largest table
                num_rows = len(table.get("rows", []))
                num_cols = len(table.get("headers", []))
                if (
                    num_rows * num_cols
                    > summary["largest_table"]["rows"]
                    * summary["largest_table"]["columns"]
                ):
                    summary["largest_table"] = {
                        "rows": num_rows,
                        "columns": num_cols,
                        "page": page,
                        "context": table.get("context"),
                        "section": table.get("section"),
                    }

        # Convert set to list for JSON serialization
        summary["table_contexts"] = list(summary["table_contexts"])

        return summary

    def get_tables_as_json(self) -> List[Dict]:
        """
        Extract tables from markdown content and return as JSON.

        Returns:
            List of dictionaries containing table data with headers and rows.

        Raises:
            TypeError: If markdown_content is not a string
        """
        if not isinstance(self.markdown_content, str):
            raise TypeError("Markdown content must be a string")

        tables = []
        table_elements = self._soup.find_all("table")

        for table in table_elements:
            try:
                # Get headers
                headers = []
                header_row = table.find("tr")
                if header_row:
                    headers = [
                        (
                            text_processors.clean_text(th.get_text())
                            if th.get_text().strip()
                            else ""
                        )
                        for th in header_row.find_all(["th", "td"])
                    ]

                # Skip tables without headers
                if not headers:
                    continue

                # Get rows
                rows = []
                data_rows = table.find_all("tr")[1:]  # Skip header row
                for row in data_rows:
                    cells = row.find_all("td")
                    # Handle rows with fewer/more columns than headers
                    row_data = {}
                    for i, header in enumerate(headers):
                        cell_value = ""
                        if i < len(cells):
                            cell_value = text_processors.clean_text(cells[i].get_text())
                        row_data[header] = cell_value
                    # Only add rows that have at least one non-empty cell
                    if any(value.strip() for value in row_data.values()):
                        rows.append(row_data)

                # Add table if it has headers and at least one data row
                if headers and rows:
                    tables.append({"headers": headers, "rows": rows})
            except Exception:
                continue  # Skip malformed tables

        return tables

    def _is_valid_table_structure(self, table) -> bool:
        """
        Check if the table has a valid markdown structure.

        Args:
            table: BeautifulSoup table element

        Returns:
            bool: True if table structure is valid, False otherwise
        """
        try:
            rows = table.find_all("tr")
            if not rows:  # Need at least one row
                return False

            # Get header row
            header_row = rows[0]
            headers = header_row.find_all(["th", "td"])
            if not headers:
                return False

            # All data rows should have cells (even if empty)
            for row in rows[1:]:
                if not row.find_all("td"):
                    return False

            return True
        except Exception:
            return False

    def json_to_markdown(self, tables: List[Dict]) -> str:
        """
        Convert JSON table data back to markdown format.

        Example input format:
        [
            {
                "headers": ["Name", "Age", "City"],
                "rows": [
                    {"Name": "John", "Age": "30", "City": "New York"},
                    {"Name": "Alice", "Age": "25", "City": "London"}
                ]
            }
        ]

        Args:
            tables: List of dictionaries containing table data with headers and rows

        Returns:
            Markdown string representation of the tables
            Empty string if input is invalid or empty

        Raises:
            TypeError: If tables is not a list
        """
        if not isinstance(tables, list):
            raise TypeError("Tables must be provided as a list")

        if not tables:
            return ""

        markdown_tables = []

        for table in tables:
            try:
                # Validate table structure
                if not isinstance(table, dict):
                    continue

                if "headers" not in table or "rows" not in table:
                    continue

                headers = table["headers"]
                if not isinstance(headers, list) or not headers:
                    continue

                rows = table["rows"]
                if not isinstance(rows, list):
                    continue

                # Build header row
                md_table = "| " + " | ".join(str(h) for h in headers) + " |\n"

                # Build separator row
                md_table += "| " + " | ".join("---" for _ in headers) + " |\n"

                # Build data rows
                for row in rows:
                    if not isinstance(row, dict):
                        continue

                    row_values = []
                    for header in headers:
                        # Use empty string for missing values
                        value = str(row.get(header, ""))
                        row_values.append(value)
                    md_table += "| " + " | ".join(row_values) + " |\n"

                markdown_tables.append(md_table)
            except Exception:
                # Skip any table that causes errors
                continue

        return "\n\n".join(markdown_tables)

    def extract_all_content(self) -> Dict[str, Any]:
        """
        Extract all content from the markdown document in a structured format.

        Returns:
            Dict containing:
            - document_info: Basic document information
            - content: Parsed content with sections
            - tables: Table data and summary
            - lists: List data and summary
            - metadata: Document metadata
        """
        # Parse the main content
        parsed = self.parse()

        # Initialize containers
        tables = []
        lists = []
        parsed_content = []

        def process_content(items, current_path=None):
            if current_path is None:
                current_path = []

            for item in items:
                if item.get("type") == "table":
                    tables.append(item)
                elif item.get("type") == "list":
                    lists.append(item)
                parsed_content.append(item)

        process_content(parsed["content"])

        # Organize tables by section
        tables_by_section = {}
        for table in tables:
            section = table.get("section", "Unknown")
            if section not in tables_by_section:
                tables_by_section[section] = []
            tables_by_section[section].append(table)

        # Organize lists by section
        lists_by_section = {}
        for lst in lists:
            section = lst.get("section", "Unknown")
            if section not in lists_by_section:
                lists_by_section[section] = []
            lists_by_section[section].append(lst)

        # Extract key-value pairs by section
        key_values_by_section = {}
        for item in parsed_content:
            if item.get("type") == "key_value":
                section = item.get("section", "Unknown")
                if section not in key_values_by_section:
                    key_values_by_section[section] = {}
                key_values_by_section[section][item["key"]] = item["value"]

        return {
            "document_info": {
                "total_sections": len(self._get_document_sections()),
                "total_tables": len(tables),
                "total_lists": len(lists),  # Include total lists
                "has_header": bool(
                    parsed_content and parsed_content[0].get("type") == "heading"
                ),
                "has_footer": bool(
                    parsed_content
                    and parsed_content[-1].get("type") in ["paragraph", "list"]
                ),
            },
            "content": {
                "sections": self._get_document_sections(),
                "parsed_content": parsed_content,
                "key_values": key_values_by_section,
            },
            "tables": {
                "data": tables_by_section,
                "summary": {
                    "total_tables": len(tables),
                    "tables_by_page": {
                        section: len(tables)
                        for section, tables in tables_by_section.items()
                    },
                },
            },
            "lists": {
                "data": lists_by_section,
                "summary": {
                    "total_lists": len(lists),  # Include total lists
                    "lists_by_section": {
                        section: len(section_lists)
                        for section, section_lists in lists_by_section.items()
                    },
                },
            },
            "metadata": parsed.get("metadata", {}),
        }

    def _get_current_section_path(self) -> List[str]:
        """Get the current section path as a list of section titles."""
        return self._section_path.copy()

    async def process_with_llm(
        self,
        provider: LLMProvider = LLMProvider.CLAUDE,
        custom_prompt: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Process document content with LLM using the llm_processors module.

        Args:
            provider (LLMProvider): The LLM provider to use
            custom_prompt (Optional[str]): Custom prompt to use instead of default
            model (Optional[str]): Specific model to use. Defaults to:
                - OpenAI: 'gpt-4'
                - Anthropic: 'claude-3-sonnet'

        Returns:
            Union[str, Dict[str, Any]]: The processed response from the LLM or error
            information

        Raises:
            ValueError: If the provider is not supported or API key is not set
            NotImplementedError: If using an unimplemented provider like Ollama
        """
        try:
            components = self.extract_document_components()
            prompt = custom_prompt or llm_processors.get_default_prompt(components)

            if provider == LLMProvider.CLAUDE:
                model = model or "claude-3-5-sonnet-20241022"
                result = await llm_processors.process_with_claude(prompt, model=model)
                return result

            elif provider == LLMProvider.OPENAI:
                model = model or "gpt-4o"
                result = await llm_processors.process_with_openai(prompt, model=model)
                return result

            elif provider == LLMProvider.OLLAMA:
                raise NotImplementedError("Ollama processing not yet implemented")
            else:
                raise ValueError(f"Unsupported LLM provider: {provider}")

        except ValueError:
            raise
        except NotImplementedError:
            raise
        except Exception as e:
            return {"error": str(e)}

    # Type aliases for clarity
    ASTNode = Dict[str, Any]
    ASTNodeList = List[ASTNode]

    def markdown_to_ast(self) -> ASTNode:
        """
        Convert markdown text to an abstract syntax tree (AST) in JSON format.

        Args:
            markdown_text: Input markdown text

        Returns:
            JSON-compatible dict representing the AST
        """
        # Initialize markdown parser with all features enabled
        md = MarkdownIt("commonmark", {"html": True, "typographer": True})

        # Enable tables plugin
        md.enable("table")

        # Parse markdown to tokens
        tokens = md.parse(self.markdown_content)

        # Convert tokens to AST
        document = {"type": "document", "children": []}

        # Stack for tracking parent nodes during tree construction
        stack = [document]

        # Keep track of list state
        list_state = {
            "in_list": False,
            "list_node": None,
            "item_node": None,
            "ordered": False,
            "level": 0,
            "prev_level": 0,
        }

        for token in tokens:
            current_parent = stack[-1]

            if token.type == "heading_open":
                heading_node = {
                    "type": "heading",
                    "depth": int(token.tag[1]),  # Extract level from h1, h2, etc.
                    "children": [],
                }
                current_parent["children"].append(heading_node)
                stack.append(heading_node)

            elif token.type == "heading_close":
                stack.pop()

            elif token.type == "paragraph_open":
                para_node = {"type": "paragraph", "children": []}
                current_parent["children"].append(para_node)
                stack.append(para_node)

            elif token.type == "paragraph_close":
                stack.pop()

            elif token.type == "bullet_list_open" or token.type == "ordered_list_open":
                is_ordered = token.type == "ordered_list_open"
                list_node = {"type": "list", "ordered": is_ordered, "children": []}

                # Handle list attributes
                if is_ordered and token.attrs and "start" in token.attrs:
                    list_node["start"] = token.attrs["start"]

                current_parent["children"].append(list_node)
                stack.append(list_node)

                # Update list state
                list_state["in_list"] = True
                list_state["list_node"] = list_node
                list_state["ordered"] = is_ordered

            elif (
                token.type == "bullet_list_close" or token.type == "ordered_list_close"
            ):
                stack.pop()

                # Reset list state if we're at the top level
                if len([t for t in stack if t.get("type") == "list"]) == 0:
                    list_state["in_list"] = False
                    list_state["list_node"] = None

            elif token.type == "list_item_open":
                item_node = {"type": "list_item", "children": []}
                current_parent["children"].append(item_node)
                stack.append(item_node)
                list_state["item_node"] = item_node

            elif token.type == "list_item_close":
                stack.pop()
                list_state["item_node"] = None

            elif token.type == "code_block":
                code_node = {
                    "type": "code_block",
                    "lang": token.info.strip() if token.info else None,
                    "value": token.content,
                }
                current_parent["children"].append(code_node)

            elif token.type == "fence":
                code_node = {
                    "type": "code_block",
                    "lang": token.info.strip() if token.info else None,
                    "value": token.content,
                }
                current_parent["children"].append(code_node)

            elif token.type == "hr":
                hr_node = {"type": "thematic_break"}
                current_parent["children"].append(hr_node)

            elif token.type == "blockquote_open":
                blockquote_node = {"type": "blockquote", "children": []}
                current_parent["children"].append(blockquote_node)
                stack.append(blockquote_node)

            elif token.type == "blockquote_close":
                stack.pop()

            elif token.type == "table_open":
                table_node = {"type": "table", "children": []}
                current_parent["children"].append(table_node)
                stack.append(table_node)

            elif token.type == "table_close":
                stack.pop()

            elif token.type == "thead_open":
                thead_node = {"type": "table_head", "children": []}
                current_parent["children"].append(thead_node)
                stack.append(thead_node)

            elif token.type == "thead_close":
                stack.pop()

            elif token.type == "tbody_open":
                tbody_node = {"type": "table_body", "children": []}
                current_parent["children"].append(tbody_node)
                stack.append(tbody_node)

            elif token.type == "tbody_close":
                stack.pop()

            elif token.type == "tr_open":
                tr_node = {"type": "table_row", "children": []}
                current_parent["children"].append(tr_node)
                stack.append(tr_node)

            elif token.type == "tr_close":
                stack.pop()

            elif token.type == "th_open" or token.type == "td_open":
                is_header = token.type == "th_open"
                align = None

                # Parse alignment from style or attrs
                if token.attrs:
                    if "style" in token.attrs:
                        style = token.attrs["style"]
                        if "text-align:right" in style:
                            align = "right"
                        elif "text-align:center" in style:
                            align = "center"
                        elif "text-align:left" in style:
                            align = "left"
                    elif "align" in token.attrs:
                        align = token.attrs["align"]

                cell_node = {"type": "table_cell", "header": is_header, "children": []}

                if align:
                    cell_node["align"] = align

                current_parent["children"].append(cell_node)
                stack.append(cell_node)

            elif token.type == "th_close" or token.type == "td_close":
                stack.pop()

            elif token.type == "inline":
                # Process inline content
                self.process_inline_content(token, current_parent)

        return document

    def process_inline_content(self, token: Token, parent_node: ASTNode) -> None:
        """Process inline markdown content within a block element."""
        if not token.children:
            return

        current_parent = parent_node
        node_stack = [parent_node]

        for child in token.children:
            if child.type == "text":
                text_node = {"type": "text", "value": child.content}
                current_parent["children"].append(text_node)

            elif child.type == "code_inline":
                code_node = {"type": "inlineCode", "value": child.content}
                current_parent["children"].append(code_node)

            elif child.type == "strong_open":
                strong_node = {"type": "strong", "children": []}
                current_parent["children"].append(strong_node)
                node_stack.append(strong_node)
                current_parent = strong_node

            elif child.type == "strong_close":
                if len(node_stack) > 1:
                    node_stack.pop()
                    current_parent = node_stack[-1]

            elif child.type == "em_open":
                em_node = {"type": "emphasis", "children": []}
                current_parent["children"].append(em_node)
                node_stack.append(em_node)
                current_parent = em_node

            elif child.type == "em_close":
                if len(node_stack) > 1:
                    node_stack.pop()
                    current_parent = node_stack[-1]

            elif child.type == "link_open":
                link_node = {
                    "type": "link",
                    "url": child.attrs.get("href", ""),
                    "title": child.attrs.get("title"),
                    "children": [],
                }
                current_parent["children"].append(link_node)
                node_stack.append(link_node)
                current_parent = link_node

            elif child.type == "link_close":
                if len(node_stack) > 1:
                    node_stack.pop()
                    current_parent = node_stack[-1]

            elif child.type == "image":
                image_node = {
                    "type": "image",
                    "url": child.attrs.get("src", ""),
                    "alt": child.attrs.get("alt", ""),
                    "title": child.attrs.get("title"),
                }
                current_parent["children"].append(image_node)

            elif child.type == "softbreak":
                break_node = {"type": "softbreak"}
                current_parent["children"].append(break_node)

            elif child.type == "hardbreak":
                break_node = {"type": "hardbreak"}
                current_parent["children"].append(break_node)

    def ast_to_markdown(self, ast: ASTNode) -> str:
        """
        Convert an AST back to markdown text.

        Args:
            ast: The abstract syntax tree as a JSON-compatible dict

        Returns:
            Markdown text
        """
        if ast["type"] != "document":
            raise ValueError("AST must have 'document' as the root type")

        result = []
        for child in ast.get("children", []):
            result.append(self.node_to_markdown(child))

        return "".join(result)

    def node_to_markdown(self, node: ASTNode) -> str:
        """Convert a single AST node to markdown."""
        node_type = node.get("type", "")

        if node_type == "text":
            return node.get("value", "")

        elif node_type == "heading":
            depth = node.get("depth", 1)
            content = "".join(
                self.node_to_markdown(child) for child in node.get("children", [])
            )
            return f"{'#' * depth} {content}\n\n"

        elif node_type == "paragraph":
            content = "".join(
                self.node_to_markdown(child) for child in node.get("children", [])
            )
            return f"{content}\n\n"

        elif node_type == "list":
            content = []
            is_ordered = node.get("ordered", False)
            start = node.get("start", 1) if is_ordered else None

            for i, item in enumerate(node.get("children", [])):
                if item.get("type") == "list_item":
                    marker = f"{(start or 1) + i}." if is_ordered else "-"
                    item_content = "".join(
                        self.node_to_markdown(child)
                        for child in item.get("children", [])
                    )

                    # Process multi-line content in list items
                    lines = item_content.split("\n")
                    first_line = lines[0].strip()
                    rest_lines = "\n".join(
                        "    " + line for line in lines[1:] if line.strip()
                    )

                    if rest_lines:
                        content.append(f"{marker} {first_line}\n{rest_lines}")
                    else:
                        content.append(f"{marker} {first_line}")

            return "\n".join(content) + "\n\n"

        elif node_type == "code_block":
            lang = node.get("lang", "")
            value = node.get("value", "")
            if lang:
                return f"```{lang}\n{value}\n```\n\n"
            else:
                return f"```\n{value}\n```\n\n"

        elif node_type == "thematic_break":
            return "---\n\n"

        elif node_type == "blockquote":
            content = "".join(
                self.node_to_markdown(child) for child in node.get("children", [])
            )
            # Add > to each line
            quoted_content = "\n".join(
                f"> {line}" for line in content.split("\n") if line.strip()
            )
            return f"{quoted_content}\n\n"

        elif node_type == "strong":
            content = "".join(
                self.node_to_markdown(child) for child in node.get("children", [])
            )
            return f"**{content}**"

        elif node_type == "emphasis":
            content = "".join(
                self.node_to_markdown(child) for child in node.get("children", [])
            )
            return f"*{content}*"

        elif node_type == "inlineCode":
            return f"`{node.get('value', '')}`"

        elif node_type == "link":
            content = "".join(
                self.node_to_markdown(child) for child in node.get("children", [])
            )
            url = node.get("url", "")
            title = node.get("title", "")
            if title:
                return f'[{content}]({url} "{title}")'
            else:
                return f"[{content}]({url})"

        elif node_type == "image":
            alt = node.get("alt", "")
            url = node.get("url", "")
            title = node.get("title", "")
            if title:
                return f'![{alt}]({url} "{title}")'
            else:
                return f"![{alt}]({url})"

        elif node_type == "softbreak":
            return " "

        elif node_type == "hardbreak":
            return "  \n"

        # Handle table nodes
        elif node_type == "table":
            rows = []

            for child in node.get("children", []):
                if child.get("type") == "table_head":
                    # Process header row
                    for row_node in child.get("children", []):
                        if row_node.get("type") == "table_row":
                            header_cells = []
                            alignments = []

                            for cell in row_node.get("children", []):
                                if cell.get("type") == "table_cell":
                                    cell_content = "".join(
                                        self.node_to_markdown(c)
                                        for c in cell.get("children", [])
                                    )
                                    header_cells.append(cell_content)
                                    alignments.append(cell.get("align", "left"))

                            if header_cells:
                                rows.append("| " + " | ".join(header_cells) + " |")

                                # Generate delimiter row
                                delimiters = []
                                for align in alignments:
                                    if align == "center":
                                        delimiters.append(":---:")
                                    elif align == "right":
                                        delimiters.append("---:")
                                    else:  # left or default
                                        delimiters.append(":---")

                                rows.append("| " + " | ".join(delimiters) + " |")

                elif child.get("type") == "table_body":
                    # Process body rows
                    for row_node in child.get("children", []):
                        if row_node.get("type") == "table_row":
                            body_cells = []

                            for cell in row_node.get("children", []):
                                if cell.get("type") == "table_cell":
                                    cell_content = "".join(
                                        self.node_to_markdown(c)
                                        for c in cell.get("children", [])
                                    )
                                    body_cells.append(cell_content)

                            if body_cells:
                                rows.append("| " + " | ".join(body_cells) + " |")

            return "\n".join(rows) + "\n\n"

        # Default case
        return ""
