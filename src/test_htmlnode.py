import unittest

from htmlnode import *
from textnode import TextNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
    def test_normal_text(self):
        """Test converting normal text node to HTML node."""
        text_node = TextNode("Hello, world!", TextType.NORMAL) 
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {})
 
    def test_bold_text(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})
 
    def test_italic_text(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, {})
    
    def test_code_text(self):
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")
        self.assertEqual(html_node.props, {})

    def test_link_text(self):
        text_node = TextNode("Visit Google", TextType.LINKS, url="https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Visit Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_text(self):
        text_node = TextNode("Profile picture", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"alt": "Profile picture", "src": "https://example.com/image.jpg"})

    def test_missing_url_for_link(self):
        text_node = TextNode("Bad link", TextType.LINKS)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Bad link")
        self.assertEqual(html_node.props, {"href": None})
"""    
    def test_missing_url_for_image(self):
        text_node = TextNode("Missing image", TextType.IMAGE)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.attributes, {"alt": "Missing image", "src": None})
    
    def test_empty_text(self):
        text_node = TextNode("", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.attributes, {})
    
    def test_exception_for_unknown_type(self):
        # Create a text node with a text_type attribute that doesn't match any case
        class UnknownTextType(Enum):
            UNKNOWN = auto()
            
        text_node = TextNode("Test")
        text_node.text_type = UnknownTextType.UNKNOWN
        
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        
        self.assertTrue("Unknown Type or missing type" in str(context.exception))
"""

if __name__ == "__main__":
    unittest.main()
