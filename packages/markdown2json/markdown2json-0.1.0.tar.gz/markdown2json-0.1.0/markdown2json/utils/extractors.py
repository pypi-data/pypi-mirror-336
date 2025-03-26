"""
markdown2json.utils.extractors
~~~~~~~~~~~~~~~~~~~~~~~~~~

Utility functions for extracting and analyzing components from markdown documents.
These functions handle the extraction of specific elements like links, images,
and tables, along with their contextual analysis.

Key Features:
    - Link extraction with metadata
    - Image extraction with attributes
    - Table context analysis
    - Semantic role detection

Example:
    >>> from markdown2json.utils.extractors import extract_links,
    determine_table_context
    >>> links = extract_links(soup_element)
    >>> table_context = determine_table_context(table_data)
"""

from typing import Dict, List, Any
from bs4 import Tag


def extract_links(element: Tag) -> List[Dict[str, str]]:
    """
    Extract links and their metadata from an HTML element.

    This function processes anchor tags within the given element and extracts
    their text content, URL, and title attributes.

    Args:
        element (Tag): BeautifulSoup Tag element to extract links from

    Returns:
        List[Dict[str, str]]: List of dictionaries containing link information:
            - text: The visible text of the link
            - url: The href attribute value
            - title: The title attribute value (if present)

    Example:
        >>> links = extract_links(soup.find('div'))
        >>> print(links)
        [{'text': 'Example', 'url': 'https://example.com', 'title': 'Visit Example'}]
    """
    links = []
    if element:
        for link in element.find_all("a"):
            links.append(
                {
                    "text": link.get_text().strip(),
                    "url": link.get("href", ""),
                    "title": link.get("title", ""),
                }
            )
    return links


def extract_images(element: Tag) -> List[Dict[str, str]]:
    """
    Extract images and their attributes from an HTML element.

    This function processes img tags within the given element and extracts
    their alt text, source URL, and title attributes.

    Args:
        element (Tag): BeautifulSoup Tag element to extract images from

    Returns:
        List[Dict[str, str]]: List of dictionaries containing image information:
            - alt: The alt text of the image
            - src: The source URL
            - title: The title attribute value (if present)

    Example:
        >>> images = extract_images(soup.find('div'))
        >>> print(images)
        [{'alt': 'Logo', 'src': '/images/logo.png', 'title': 'Company Logo'}]
    """
    images = []
    if element:
        for img in element.find_all("img"):
            images.append(
                {
                    "alt": img.get("alt", ""),
                    "src": img.get("src", ""),
                    "title": img.get("title", ""),
                }
            )
    return images


def determine_table_context(table: Dict[str, Any]) -> str:
    """
    Determine the semantic context/purpose of a table based on its content.

    This function analyzes table headers and content to categorize the table's
    purpose (e.g., financial, timeline, items list).

    Args:
        table (Dict[str, Any]): Dictionary containing table data with structure:
            {
                "data": {
                    "headers": List[str],
                    "rows": List[Dict]
                }
            }

    Returns:
        str: The determined context category:
            - "financial": Tables containing monetary information
            - "timeline": Tables with date/time information
            - "items": Tables listing products or items
            - "general": Tables that don't fit specific categories

    Example:
        >>> context = determine_table_context({"data": {"headers": ["Item", "Price"]}})
        >>> print(context)
        'financial'
    """
    headers = table["data"].get("headers", [])
    headers_text = " ".join(headers).lower()

    # Financial tables
    if any(
        word in headers_text
        for word in ["amount", "price", "cost", "charge", "payment", "balance"]
    ):
        return "financial"

    # Timeline/schedule tables
    elif any(
        word in headers_text
        for word in ["date", "period", "time", "schedule", "deadline"]
    ):
        return "timeline"

    # Item/product tables
    elif any(
        word in headers_text
        for word in ["item", "description", "product", "service", "quantity"]
    ):
        return "items"

    # Default category
    return "general"


def extract_table_metadata(table: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract metadata and statistics about a table.

    This function analyzes a table's structure and content to provide
    useful metadata about its composition and characteristics.

    Args:
        table (Dict[str, Any]): Dictionary containing table data

    Returns:
        Dict[str, Any]: Dictionary containing table metadata:
            - row_count: Number of data rows
            - column_count: Number of columns
            - empty_cells: Count of empty cells
            - numeric_columns: List of columns containing numeric data
            - date_columns: List of columns containing dates
            - has_headers: Whether the table has header row

    Example:
        >>> metadata = extract_table_metadata(table_data)
        >>> print(metadata['row_count'])
        5
    """
    metadata = {
        "row_count": len(table.get("data", {}).get("rows", [])),
        "column_count": len(table.get("data", {}).get("headers", [])),
        "empty_cells": 0,
        "numeric_columns": [],
        "date_columns": [],
        "has_headers": bool(table.get("data", {}).get("headers", [])),
    }

    # Analyze columns
    headers = table.get("data", {}).get("headers", [])
    rows = table.get("data", {}).get("rows", [])

    for col_idx, header in enumerate(headers):
        numeric_count = 0
        date_count = 0
        empty_count = 0

        for row in rows:
            cell_value = row[col_idx] if col_idx < len(row) else ""

            if not cell_value:
                empty_count += 1
                continue

            # Check for numeric values
            try:
                float(cell_value)
                numeric_count += 1
            except ValueError:
                # Check for date patterns
                if any(
                    date_pattern in cell_value.lower()
                    for date_pattern in [
                        "date",
                        "jan",
                        "feb",
                        "mar",
                        "apr",
                        "may",
                        "jun",
                        "jul",
                        "aug",
                        "sep",
                        "oct",
                        "nov",
                        "dec",
                    ]
                ):
                    date_count += 1

        metadata["empty_cells"] += empty_count

        # Determine column type based on majority content
        if numeric_count > len(rows) * 0.5:
            metadata["numeric_columns"].append(header)
        elif date_count > len(rows) * 0.5:
            metadata["date_columns"].append(header)

    return metadata
