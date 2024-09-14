import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_text_dif(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text, "This is a text node")

    def text_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "normal")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a text node", "text"))
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.tag, None)

    def test_bold_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a text node", "bold"))
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.tag, "b")

    def test_italic_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a text node", "italic"))
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.tag, "i")

    def test_code_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a text node", "code"))
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.tag, "code")

    def test_link_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a text node", "link"))
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.tag, "a")

    def test_image_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("", "image"))
        self.assertEqual(node.value, "")
        self.assertEqual(node.tag, "img")


if __name__ == "__main__":
    unittest.main()
