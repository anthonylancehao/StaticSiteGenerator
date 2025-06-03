import unittest
from textnode import TextNode, TextType
from markdown_splitters import split_nodes_image, split_nodes_link

class TestMarkdownSplitters(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
        )

    def test_split_links(self):
        node = TextNode(
            "Here's a link [to Google](https://www.google.com) and [to GitHub](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Here's a link ", TextType.TEXT),
                TextNode("to Google", TextType.LINK, "https://www.google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to GitHub", TextType.LINK, "https://github.com"),
            ],
        )

    def test_no_images(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [node])

    def test_no_links(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [node])

if __name__ == "__main__":
    unittest.main()

