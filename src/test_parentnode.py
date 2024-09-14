import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
  def test_simple_leaf_children(self):
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

  def test_leaf_children_with_props(self):
    node = ParentNode(
        "div",
        [
            LeafNode("b", "Bold text", {
              "href": "https://www.google.com"
            }),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
        ],
    )
    
    self.assertEqual(node.to_html(), '<div><b href="https://www.google.com">Bold text</b>Normal text<i>italic text</i></div>')
    

if __name__ == "__main__":
  unittest.main()
