import unittest
from utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        md = "# Hello World\nSome text"
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_strips_whitespace(self):
        md = "#   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_no_h1(self):
        md = "## Subtitle\nNo h1 here"
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
