import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_eq(self):
    node = HTMLNode("This is a HTML node", "This is my text", None, {
      "href": "https://www.google.com", 
      "target": "_blank",
    })
    node2 = HTMLNode("This is a HTML node", "This is my text", None, {
      "href": "https://www.google.com", 
      "target": "_blank",
    })
    self.assertEqual(node.value, node2.value)
  
  def test_props_to_html(self):
    node = HTMLNode("This is a HTML node", "This is my text", None, {
      "href": "https://www.google.com", 
      "target": "_blank",
    })
    self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
  unittest.main()
