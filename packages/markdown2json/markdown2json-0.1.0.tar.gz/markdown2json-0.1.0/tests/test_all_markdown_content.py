import unittest
from markdown2json.parser import MarkdownToJSON
from markdown2json.utils import text_processors, extractors
from bs4 import BeautifulSoup


class TestMarkdownToJSON(unittest.TestCase):
    def setUp(self):
        self.sample_markdown = """# Test Document

## Section 1
This is a test paragraph.

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

## Section 2
Another paragraph here.
"""
        self.parser = MarkdownToJSON(self.sample_markdown)

    def test_extract_all_content(self):
        content = self.parser.extract_all_content()

        # Verify basic structure
        self.assertIn("document_info", content)
        self.assertIn("content", content)
        self.assertIn("tables", content)
        self.assertIn("metadata", content)

        # Verify document info
        self.assertGreater(content["document_info"]["total_sections"], 0)
        self.assertIsInstance(content["document_info"]["total_tables"], int)
        self.assertIsInstance(content["document_info"]["has_header"], bool)
        self.assertIsInstance(content["document_info"]["has_footer"], bool)

        # Verify content sections
        self.assertGreater(len(content["content"]["sections"]), 0)
        section_titles = [
            section.get("title") for section in content["content"]["sections"]
        ]
        self.assertIn("Test Document", section_titles)

        # Verify table extraction
        self.assertEqual(content["tables"]["summary"]["total_tables"], 1)

    def test_extract_document_components(self):
        components = self.parser.extract_document_components()

        self.assertIn("header_info", components)
        self.assertIn("footer_info", components)
        self.assertIn("tables", components)
        self.assertIn("metadata", components)
        self.assertIn("misc_details", components)

    def test_get_tables_as_json(self):
        tables = self.parser.get_tables_as_json()

        self.assertIsInstance(tables, list)
        self.assertEqual(len(tables), 1)
        self.assertIn("headers", tables[0])
        self.assertIn("rows", tables[0])
        self.assertEqual(tables[0]["headers"], ["Header 1", "Header 2"])

    def test_extract_tables_by_page(self):
        tables = self.parser.extract_tables_by_page()

        self.assertIsInstance(tables, dict)
        self.assertGreater(len(tables), 0)

        # Check first page tables
        first_page = next(iter(tables.values()))
        self.assertIsInstance(first_page, list)
        self.assertGreater(len(first_page), 0)
        self.assertIn("headers", first_page[0])
        self.assertIn("rows", first_page[0])

    def test_get_table_summary(self):
        summary = self.parser.get_table_summary()

        self.assertIn("total_tables", summary)
        self.assertIn("tables_by_page", summary)
        self.assertIn("table_contexts", summary)
        self.assertIn("largest_table", summary)
        self.assertEqual(summary["total_tables"], 1)

    def test_text_processing(self):
        # Test text cleaning
        text = "  Test   String  \n with spaces  "
        cleaned = text_processors.clean_text(text)
        self.assertEqual(cleaned, "Test String with spaces")

    def test_extractors(self):
        html = """<div>
            <a href="test.com">Link</a>
            <img src="test.jpg" alt="Test">
        </div>"""
        soup = BeautifulSoup(html, "html.parser")

        # Test link extraction
        links = extractors.extract_links(soup)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["url"], "test.com")

        # Test image extraction
        images = extractors.extract_images(soup)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["src"], "test.jpg")


if __name__ == "__main__":
    unittest.main()
