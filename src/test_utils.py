import unittest

import utils
from htmlnode import HTMLNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestHTMLNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = utils.split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = utils.extract_markdown_links(text)
        self.assertEqual(result[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(
            result[1], ("to youtube", "https://www.youtube.com/@bootdotdev")
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = utils.extract_markdown_images(text)
        self.assertEqual(result[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(result[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = utils.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = utils.text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        list_of_blocks = utils.markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            list_of_blocks,
        )

    def test_block_to_block_type(self):
        markdown_1 = "### This is a heading"
        markdown_2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        markdown_3 = """
- Item 1
- Item 2
* Another item
+ Yet another"""
        markdown_4 = """
1. Item 1
2. Item 2
3. Another item
4. Yet another"""
        self.assertEqual(utils.block_to_block_type(markdown_1), "heading 3")
        self.assertEqual(utils.block_to_block_type(markdown_2), "pharagraph")
        self.assertEqual(utils.block_to_block_type(markdown_3), "unordered_list")
        self.assertEqual(utils.block_to_block_type(markdown_4), "ordered_list")

    def test_markdown_to_html_node(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is the first list item in a list block
2. This is a list item
3. This is another list item

```This is a code block```

>This is a blockquote block
"""
        markdown_1 = "# This is a heading"
        markdown_2 = "# This is a heading"
        self.assertEqual(
            repr(utils.markdown_to_html_node(markdown_1)),
            repr(HTMLNode("div", "", [HTMLNode("h1", "# This is a heading")])),
        )


if __name__ == "__main__":
    unittest.main()
