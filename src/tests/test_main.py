import unittest

from src.main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_single_line(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        markdown = "#   Hello world   "
        self.assertEqual(extract_title(markdown), "Hello world")

    def test_extract_title_raises_without_h1(self):
        markdown = "## Subtitle\n\nParagraph text"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
