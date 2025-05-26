from textnode import *

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props = ""
        for key in self.props:
            props += f' {key}="{self.props[key]}"'
        return props

    def __eq__(self, node):
        return (
            self.tag == node.tag
            and self.value == node.value
            and self.children == node.children
            and self.props == node.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = {}):
        super().__init__(tag, value, [], props)

    def to_htlm(self):
        if self.value == "" or self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        if self.props != None:
            return f'"<{self.tag}{self.props}>{self.value}</{self.tag}>"'
        else:
            return f'"<{self.tag}>{self.value}</{self.tag}>"'
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children = []):
        super().__init__(tag, children)

    def to_html(self):
        if self.tag == "" or self.tag == None:
            raise ValueError("No tags given")
        if self.children == "" or self.children == None or self.children == []:
            raise ValueError("No children given")
        
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"alt":text_node.text, "src":text_node.url})
    else:
        raise Exception("Unknown Type or missing type")
    
