import unittest
from markdown_extractors import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "![img](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("img", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![one](url1) and ![two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "[link](https://www.boot.dev)"
        expected = [("link", "https://www.boot.dev")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[one](url1) and [two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_no_false_positives_on_images(self):
        text = "![notalink](image.png)"
        self.assertListEqual(extract_markdown_links(text), [])

    def test_no_false_positives_on_links(self):
        text = "[notanimage](page.html)"
        self.assertListEqual(extract_markdown_images(text), [])

if __name__ == "__main__":
    unittest.main()

