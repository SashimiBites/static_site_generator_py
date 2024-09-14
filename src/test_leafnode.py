import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_eq(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.value, node2.value)
  
  def test_if_renders_properly(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
  unittest.main()
