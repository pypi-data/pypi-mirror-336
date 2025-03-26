import unittest
from markdown2json.parser import MarkdownToJSON


class TestTableExtraction(unittest.TestCase):
    def setUp(self):
        self.sample_markdown_with_tables = """# Document with Tables

## First Table
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

## Second Table
| Column A | Column B |
|----------|----------|
| Data 1   | Data 2   |

## Text Section
Some text here.

## Third Table
| Item  | Price |
|-------|-------|
| Item1 | $100  |
| Item2 | $200  |
"""
        self.parser = MarkdownToJSON(self.sample_markdown_with_tables)

    def test_extract_tables(self):
        tables = self.parser.get_tables_as_json()

        # Verify number of tables
        self.assertEqual(len(tables), 3)

        # Verify first table
        first_table = tables[0]
        self.assertEqual(first_table["headers"], ["Header 1", "Header 2", "Header 3"])
        self.assertEqual(len(first_table["rows"]), 2)
        self.assertEqual(first_table["rows"][0]["Header 1"], "Value 1")

        # Verify second table
        second_table = tables[1]
        self.assertEqual(second_table["headers"], ["Column A", "Column B"])
        self.assertEqual(len(second_table["rows"]), 1)
        self.assertEqual(second_table["rows"][0]["Column A"], "Data 1")

        # Verify third table
        third_table = tables[2]
        self.assertEqual(third_table["headers"], ["Item", "Price"])
        self.assertEqual(len(third_table["rows"]), 2)
        self.assertEqual(third_table["rows"][0]["Item"], "Item1")

    def test_extract_tables_by_page(self):
        tables_by_page = self.parser.extract_tables_by_page()

        # Verify structure
        self.assertIsInstance(tables_by_page, dict)
        self.assertGreater(len(tables_by_page), 0)

        # Get first page tables
        first_page = next(iter(tables_by_page.values()))
        self.assertIsInstance(first_page, list)
        self.assertEqual(len(first_page), 3)

        # Verify table data
        first_table = first_page[0]
        self.assertIn("headers", first_table)
        self.assertIn("rows", first_table)
        self.assertIn("context", first_table)
        self.assertIn("section", first_table)

    def test_get_table_summary(self):
        summary = self.parser.get_table_summary()

        # Verify summary structure
        self.assertIn("total_tables", summary)
        self.assertIn("tables_by_page", summary)
        self.assertIn("table_contexts", summary)
        self.assertIn("largest_table", summary)

        # Verify counts
        self.assertEqual(summary["total_tables"], 3)
        self.assertGreater(len(summary["tables_by_page"]), 0)

        # Verify largest table info
        largest = summary["largest_table"]
        self.assertIn("rows", largest)
        self.assertIn("columns", largest)
        self.assertEqual(largest["rows"], 2)  # First table has 2 rows
        self.assertEqual(largest["columns"], 3)  # First table has 3 columns

    def test_table_extraction_no_tables(self):
        markdown_content = """# Document without Tables

## Section 1
This is a test paragraph.

## Section 2
Another paragraph here.
"""
        parser = MarkdownToJSON(markdown_content)

        # Test direct table extraction
        tables = parser.get_tables_as_json()
        self.assertIsInstance(tables, list)
        self.assertEqual(len(tables), 0)

        # Test tables by page
        tables_by_page = parser.extract_tables_by_page()
        self.assertIsInstance(tables_by_page, dict)
        self.assertEqual(len(tables_by_page), 0)

        # Test summary
        summary = parser.get_table_summary()
        self.assertEqual(summary["total_tables"], 0)
        self.assertEqual(len(summary["tables_by_page"]), 0)

    def test_table_context_extraction(self):
        components = self.parser.extract_document_components()

        # Verify tables have context
        tables = components["tables"]
        for table in tables:
            self.assertIn("context", table)
            self.assertIn("path", table)

        # Verify table paths match section structure
        sections = self.parser._get_document_sections()
        section_titles = [section["title"] for section in sections]

        for table in tables:
            table_section = table["path"][-1] if table["path"] else None
            self.assertIn(table_section, section_titles)


if __name__ == "__main__":
    unittest.main()
