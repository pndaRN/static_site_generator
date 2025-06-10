from block_markdown import *
import unittest

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_single_hash(self):
        """Test heading with single #"""
        block = "# This is a heading"
        self.assertEqual(block_to_block(block), BlockType.HEADING)
    
    def test_heading_multiple_hash(self):
        """Test headings with 2-6 # characters"""
        test_cases = [
            "## Heading 2",
            "### Heading 3", 
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        for case in test_cases:
            self.assertEqual(block_to_block(case), BlockType.HEADING)

    def test_heading_no_space_after_hash(self):
        """Test that # without space is not a heading"""
        block = "#NotAHeading"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)

    def test_code_block_simple(self):
        """Test simple code block"""
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block(block), BlockType.CODE)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        block = "```python\nprint('hello')\nprint('world')\n```"
        self.assertEqual(block_to_block(block), BlockType.CODE)
    
    def test_code_block_single_line(self):
        """Test single line code block"""
        block = "```code```"
        self.assertEqual(block_to_block(block), BlockType.CODE)
    
    def test_incomplete_code_block(self):
        """Test code block missing closing backticks"""
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        """Test single line quote"""
        block = "> This is a quote"
        self.assertEqual(block_to_block(block), BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        """Test multi-line quote"""
        block = "> This is a quote\n> spanning multiple lines\n> with more text"
        self.assertEqual(block_to_block(block), BlockType.QUOTE)
    
    def test_quote_with_empty_quote_line(self):
        """Test quote with empty quote line"""
        block = "> This is a quote\n>\n> with empty line"
        self.assertEqual(block_to_block(block), BlockType.QUOTE)
    
    def test_partial_quote(self):
        """Test block where not all lines start with >"""
        block = "> This is a quote\nThis line is not quoted"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_single_item(self):
        """Test single item unordered list"""
        block = "- First item"
        self.assertEqual(block_to_block(block), BlockType.ULIST)
    
    def test_unordered_list_multiple_items(self):
        """Test multiple item unordered list"""
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block(block), BlockType.ULIST)
    
    def test_unordered_list_no_space(self):
        """Test that - without space is not unordered list"""
        block = "-Not a list item"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_partial_unordered_list(self):
        """Test block where not all lines start with -"""
        block = "- First item\nNot a list item"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_single_item(self):
        """Test single item ordered list"""
        block = "1. First item"
        self.assertEqual(block_to_block(block), BlockType.OLIST)
    
    def test_ordered_list_multiple_items(self):
        """Test multiple item ordered list"""
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block(block), BlockType.OLIST)
    
    def test_ordered_list_wrong_numbering(self):
        """Test ordered list with wrong numbering"""
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_no_space(self):
        """Test that number. without space is not ordered list"""
        block = "1.Not a list item"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_starting_wrong_number(self):
        """Test ordered list not starting with 1"""
        block = "2. Second item\n3. Third item"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_paragraph_simple(self):
        """Test simple paragraph"""
        block = "This is just a normal paragraph with some text."
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        """Test multi-line paragraph"""
        block = "This is a paragraph\nwith multiple lines\nof text."
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_paragraph_with_special_chars(self):
        """Test paragraph containing special characters"""
        block = "This paragraph has # and > and - but not at line starts"
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    
    def test_empty_block(self):
        """Test edge case with empty block"""
        block = ""
        self.assertEqual(block_to_block(block), BlockType.PARAGRAPH)
    

    if __name__ == "__main__":
        unittest.main()
