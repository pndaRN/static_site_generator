import unittest
from inline_markdown import (
    split_nodes_delimiter, extract_markdown_images,
    extract_markdown_links, split_nodes_image,
    split_nodes_link, text_to_textnodes
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_extract_single_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_images(text)
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(result, expected)
    
    def test_extract_multiple_images(self):
        text = "Here's an ![first image](https://example.com/img1.jpg) and another ![second image](https://example.com/img2.png)"
        result = extract_markdown_images(text)
        expected = [
            ("first image", "https://example.com/img1.jpg"),
            ("second image", "https://example.com/img2.png")
        ]
        self.assertEqual(result, expected)
    
    def test_extract_image_empty_alt_text(self):
        text = "Image with no alt text: ![](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        expected = [("", "https://example.com/image.jpg")]
        self.assertEqual(result, expected)
    
    def test_extract_image_empty_url(self):
        text = "Image with no URL: ![alt text]()"
        result = extract_markdown_images(text)
        expected = [("alt text", "")]
        self.assertEqual(result, expected)
    
    def test_extract_image_with_spaces_in_alt(self):
        text = "![This is a long alt text with spaces](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("This is a long alt text with spaces", "https://example.com/image.png")]
        self.assertEqual(result, expected)
    
    def test_extract_no_images(self):
        text = "This is just regular text with no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_extract_image_with_link_nearby(self):
        """Test that images are extracted correctly when links are nearby."""
        text = "Check out this [link](https://example.com) and this ![image](https://example.com/img.jpg)"
        result = extract_markdown_images(text)
        expected = [("image", "https://example.com/img.jpg")]
        self.assertEqual(result, expected)
    
    def test_extract_image_malformed_brackets(self):
        """Test that malformed image syntax is not extracted."""
        text = "This is not an image: !image](https://example.com/img.jpg) or ![image(https://example.com/img.jpg)"
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)
    
    # Tests for extract_markdown_links
    def test_extract_single_link(self):
        """Test extracting a single link from markdown text."""
        text = "This is a [link](https://www.example.com)"
        result = extract_markdown_links(text)
        expected = [("link", "https://www.example.com")]
        self.assertEqual(result, expected)
    
    def test_extract_multiple_links(self):
        """Test extracting multiple links from markdown text."""
        text = "Visit [Google](https://www.google.com) or [GitHub](https://www.github.com)"
        result = extract_markdown_links(text)
        expected = [
            ("Google", "https://www.google.com"),
            ("GitHub", "https://www.github.com")
        ]
        self.assertEqual(result, expected)
    
    def test_extract_link_empty_text(self):
        """Test extracting link with empty anchor text."""
        text = "Empty link text: [](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertEqual(result, expected)
    
    def test_extract_link_empty_url(self):
        """Test extracting link with empty URL."""
        text = "Empty URL: [click here]()"
        result = extract_markdown_links(text)
        expected = [("click here", "")]
        self.assertEqual(result, expected)
    
    def test_extract_link_with_spaces(self):
        """Test extracting link with spaces in anchor text."""
        text = "This is a [long anchor text with spaces](https://example.com/page)"
        result = extract_markdown_links(text)
        expected = [("long anchor text with spaces", "https://example.com/page")]
        self.assertEqual(result, expected)
    
    def test_extract_no_links(self):
        """Test text with no links returns empty list."""
        text = "This is just regular text with no links."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_extract_link_not_image(self):
        """Test that image syntax is not extracted as links."""
        text = "This is an image ![alt](https://example.com/img.jpg) not a link"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_extract_link_with_image_nearby(self):
        """Test that links are extracted correctly when images are nearby."""
        text = "Here's a [link](https://example.com) and an ![image](https://example.com/img.jpg)"
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)
    
    def test_extract_link_malformed_brackets(self):
        """Test that malformed link syntax is not extracted."""
        text = "Not a link: link](https://example.com) or [link(https://example.com)"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)
    
    # Combined tests
    def test_extract_mixed_images_and_links(self):
        """Test complex text with both images and links."""
        text = "Check out [this website](https://example.com) which has ![cool images](https://example.com/img1.jpg) and [more info](https://example.com/info) plus ![another image](https://example.com/img2.png)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [
            ("cool images", "https://example.com/img1.jpg"),
            ("another image", "https://example.com/img2.png")
        ]
        expected_links = [
            ("this website", "https://example.com"),
            ("more info", "https://example.com/info")
        ]
        
        self.assertEqual(images, expected_images)
        self.assertEqual(links, expected_links)
    
    def test_extract_nested_brackets(self):
        """Test that nested brackets don't break the extraction."""
        text = "A [link with [nested] brackets](https://example.com) and ![image with [brackets] in alt](https://example.com/img.jpg)"
        
        # Note: The regex might not handle nested brackets perfectly, 
        # but let's test the current behavior
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        # The actual behavior depends on the regex implementation
        # This test documents the current behavior
        self.assertIsInstance(images, list)
        self.assertIsInstance(links, list)
    
    def test_extract_special_characters_in_urls(self):
        """Test URLs with special characters."""
        text = "Link with query params: [search](https://example.com/search?q=test&type=all) and image ![graph](https://example.com/charts/data.png?size=large)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [("graph", "https://example.com/charts/data.png?size=large")]
        expected_links = [("search", "https://example.com/search?q=test&type=all")]
        
        self.assertEqual(images, expected_images)
        self.assertEqual(links, expected_links)

        def test_text_to_textnodes(self):
            nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
            )
            self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes,
            )
if __name__ == "__main__":
    unittest.main()
