from enum import Enum
from htmlnode import ParentNode
from inline_markdown import *
from textnode import * 

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "Quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"
    

def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    filtered_block = []
    for text in split_md:
        if text == "":
            continue
        text = text.strip()
        filtered_block.append(text)
    return filtered_block

def block_to_block(block):

    #Split text
    lines = block.split("\n")

    #Check for heading followed by space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        htmlnode = block_to_html_node(block)
        children.append(htmlnode)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(raw_text)
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_item =[]
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_item.append(ParentNode("li", children))
    return ParentNode("ol", html_item)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_item = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_item.append(ParentNode("li", children))
    return ParentNode("ul", html_item)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("not a vaild quote")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


