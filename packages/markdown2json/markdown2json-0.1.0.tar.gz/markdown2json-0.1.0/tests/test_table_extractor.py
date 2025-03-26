import unittest
from markdown2json.parser import MarkdownToJSON


class TestTableExtractor(unittest.TestCase):
    def setUp(self):
        # Sample markdown with multiple tables and structures
        self.test_markdown = """
# Sample Document

## Basic Table
Here's a simple table:

| Name    | Age | City     |
|---------|-----|----------|
| John    | 30  | New York |
| Alice   | 25  | London   |
| Bob     | 35  | Paris    |

## Complex Table with Empty Cells
Some context about the data:

| Category      | Count    | Score | Rating   |
|---------------|----------|-------|----------|
| Type A        | 2        | 8.5   | High     |
| Type B        |          | 7.2   | Medium   |
| Type C        | 1        |       | Low      |

## Table with Special Characters
*Note: This table contains special formatting*

| Symbol | Description | Usage Rate (%) |
|--------|-------------|----------------|
| #      | Hash        | 15%           |
| @      | At Sign     | 25%           |
| $      | Dollar      | 35%           |

## Nested Lists and Text
1. First item
   - Sub item 1
   - Sub item 2
2. Second item
   * Nested list
   * Another item

## Table with Long Content
| Column 1                  | Column 2                                    |
|--------------------------|---------------------------------------------|
| This is a long cell      | This is another long cell with more content|
| Short cell               | Medium length cell content                  |
"""

        # Invalid markdown samples
        self.invalid_table_markdown = """
# Invalid Table Test
| Invalid | Table |
| Missing | Separator |
| Row1 | Data |
"""
        self.mismatched_columns_markdown = """
# Mismatched Columns Test
| Header1 | Header2 | Header3 |
|---------|---------|---------|
| Data1   | Data2   |
| Data3   | Data4   | Data5   | Extra |
"""
        self.empty_table_markdown = """
# Empty Table Test
| | |
|-|-|
| | |
"""

        # Expected JSON structure for the first table
        self.expected_first_table = {
            "headers": ["Name", "Age", "City"],
            "rows": [
                {"Name": "John", "Age": "30", "City": "New York"},
                {"Name": "Alice", "Age": "25", "City": "London"},
                {"Name": "Bob", "Age": "35", "City": "Paris"},
            ],
        }

        # Create a minimal valid markdown for testing edge cases
        self.minimal_valid_markdown = "# Test Document\nThis is a test."

    def test_markdown_to_json_basic(self):
        """Test basic markdown to JSON conversion"""
        parser = MarkdownToJSON(self.test_markdown)
        tables = parser.get_tables_as_json()

        # Check if we got all tables
        self.assertEqual(len(tables), 4, "Should extract 4 tables")

        # Test first table structure
        first_table = tables[0]
        self.assertEqual(first_table["headers"], self.expected_first_table["headers"])
        self.assertEqual(first_table["rows"], self.expected_first_table["rows"])

    def test_empty_cells_handling(self):
        """Test handling of empty cells in tables"""
        parser = MarkdownToJSON(self.test_markdown)
        tables = parser.get_tables_as_json()

        # Get the second table (Complex Table with Empty Cells)
        complex_table = tables[1]

        # Check empty cells
        empty_cells_found = False
        for row in complex_table["rows"]:
            if "" in row.values():
                empty_cells_found = True
                break

        self.assertTrue(empty_cells_found, "Should handle empty cells")

    def test_special_characters(self):
        """Test handling of special characters in tables"""
        parser = MarkdownToJSON(self.test_markdown)
        tables = parser.get_tables_as_json()

        # Get the third table (Table with Special Characters)
        special_char_table = tables[2]

        # Check if special characters are preserved
        special_chars = ["#", "@", "$"]
        found_chars = []
        for row in special_char_table["rows"]:
            found_chars.append(row["Symbol"])

        for char in special_chars:
            self.assertIn(
                char, found_chars, f"Special character {char} should be preserved"
            )

    def test_json_to_markdown_conversion(self):
        """Test converting JSON back to markdown format"""
        # Convert sample table to markdown
        sample_tables = [
            {
                "headers": ["Test", "Data"],
                "rows": [
                    {"Test": "Value1", "Data": "Data1"},
                    {"Test": "Value2", "Data": "Data2"},
                ],
            }
        ]

        parser = MarkdownToJSON(self.minimal_valid_markdown)
        markdown_output = parser.json_to_markdown(sample_tables)

        # Basic validation of markdown format
        self.assertIn("| Test", markdown_output)
        self.assertIn("| Data", markdown_output)
        self.assertIn("Value1", markdown_output)
        self.assertIn("Value2", markdown_output)

        # Convert back to JSON and compare
        new_parser = MarkdownToJSON(markdown_output)
        converted_tables = new_parser.get_tables_as_json()

        self.assertEqual(len(converted_tables), 1)
        self.assertEqual(converted_tables[0]["headers"], sample_tables[0]["headers"])
        self.assertEqual(converted_tables[0]["rows"], sample_tables[0]["rows"])

    def test_roundtrip_conversion(self):
        """Test full roundtrip conversion (markdown -> JSON -> markdown -> JSON)"""
        # Start with original markdown
        parser = MarkdownToJSON(self.test_markdown)
        original_tables = parser.get_tables_as_json()

        # Convert to markdown
        markdown_output = parser.json_to_markdown(original_tables)

        # Convert back to JSON
        new_parser = MarkdownToJSON(markdown_output)
        converted_tables = new_parser.get_tables_as_json()

        # Compare number of tables
        self.assertEqual(len(original_tables), len(converted_tables))

        # Compare content of each table
        for orig_table, conv_table in zip(original_tables, converted_tables):
            self.assertEqual(orig_table["headers"], conv_table["headers"])
            self.assertEqual(orig_table["rows"], conv_table["rows"])

    def test_empty_input(self):
        """Test handling of empty input"""
        # Test empty string
        with self.assertRaises(ValueError):
            MarkdownToJSON("")

        # Test None input
        with self.assertRaises(TypeError):
            MarkdownToJSON(None)

        # Test whitespace only
        with self.assertRaises(ValueError):
            MarkdownToJSON("   \n   \t   ")

    def test_invalid_table_structure(self):
        """Test handling of invalid table structures"""
        # Test table without separator
        parser = MarkdownToJSON(self.invalid_table_markdown)
        tables = parser.get_tables_as_json()
        self.assertEqual(len(tables), 0, "Invalid table should be ignored")

        # Test mismatched columns
        parser = MarkdownToJSON(self.mismatched_columns_markdown)
        tables = parser.get_tables_as_json()
        if tables:
            # Check if all rows have the same number of columns as headers
            first_table = tables[0]
            header_count = len(first_table["headers"])
            for row in first_table["rows"]:
                self.assertEqual(
                    len(row),
                    header_count,
                    "Each row should have same number of columns as headers",
                )

    def test_empty_table(self):
        """Test handling of empty tables"""
        parser = MarkdownToJSON(self.empty_table_markdown)
        tables = parser.get_tables_as_json()
        if tables:
            table = tables[0]
            self.assertTrue(
                all(not header.strip() for header in table["headers"]),
                "Empty headers should be preserved",
            )
            self.assertTrue(
                all(
                    all(not value.strip() for value in row.values())
                    for row in table["rows"]
                ),
                "Empty cells should be preserved",
            )

    def test_invalid_json_to_markdown(self):
        """Test invalid inputs for JSON to markdown conversion"""
        parser = MarkdownToJSON(self.minimal_valid_markdown)

        # Test with None
        with self.assertRaises(TypeError):
            parser.json_to_markdown(None)

        # Test with empty list
        result = parser.json_to_markdown([])
        self.assertEqual(result.strip(), "", "Empty list should return empty string")

        # Test with invalid table structure
        invalid_tables = [
            {"wrong_key": "value"},  # Missing required keys
            {"headers": ["h1"], "rows": "not_a_list"},  # Invalid rows type
            {"headers": "not_a_list", "rows": []},  # Invalid headers type
            {
                "headers": [],
                "rows": [{"key": "no_matching_header"}],
            },  # Mismatched headers
        ]

        for invalid_table in invalid_tables:
            result = parser.json_to_markdown([invalid_table])
            self.assertEqual(
                result.strip(),
                "",
                f"Invalid table structure {invalid_table} should return empty string",
            )

    def test_malformed_markdown(self):
        """Test handling of malformed markdown content"""
        malformed_content = """
# Test Document
This is some text
| Broken | Table |
No separator row
| More | Content |
"""
        parser = MarkdownToJSON(malformed_content)
        tables = parser.get_tables_as_json()
        self.assertEqual(len(tables), 0, "Malformed tables should be ignored")

    def test_large_table_handling(self):
        """Test handling of large tables"""
        # Create a large table
        headers = ["Col" + str(i) for i in range(10)]
        rows = []
        for i in range(100):
            row = {header: f"Value{i}-{j}" for j, header in enumerate(headers)}
            rows.append(row)

        large_table = {"headers": headers, "rows": rows}

        parser = MarkdownToJSON(self.minimal_valid_markdown)
        markdown_output = parser.json_to_markdown([large_table])

        # Verify the output
        self.assertIsInstance(markdown_output, str)
        self.assertGreater(len(markdown_output), 0)

        # Convert back and verify structure is preserved
        new_parser = MarkdownToJSON(markdown_output)
        converted_tables = new_parser.get_tables_as_json()
        self.assertEqual(len(converted_tables), 1)
        self.assertEqual(len(converted_tables[0]["headers"]), len(headers))
        self.assertEqual(len(converted_tables[0]["rows"]), len(rows))


if __name__ == "__main__":
    unittest.main()
