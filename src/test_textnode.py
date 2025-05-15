import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        node3 = TextNode("This is a link", TextType.LINKS, "boot.dev")
        self.assertNotEqual(node, node3)
        
        node4 = TextNode("Image", TextType.IMAGE)
        node5 = TextNode("Image", TextType.IMAGE)

        self.assertEqual(node4, node5)
        self.assertNotEqual(node2, node4)

        node6 = TextNode("This is italics", TextType.ITALIC)
        node7 = TextNode("This is not", TextType.NORMAL)

        self.assertNotEqual(node6, node7)


if __name__ == "__main__":
    unittest.main()
