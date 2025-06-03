from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")
    
from textnode import TextNode, TextType
from markdown_splitters import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_bold,
    split_nodes_italic,
    split_nodes_code,
)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_bold(nodes)
    nodes = split_nodes_italic(nodes)
    nodes = split_nodes_code(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    # Split on two newlines (empty line)
    raw_blocks = markdown.split('\n\n')

    # Strip whitespace and filter out empty blocks
    blocks = [block.strip() for block in raw_blocks if block.strip() != '']

    return blocks

from enum import Enum, auto
import re

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def block_to_block_type(block):
    lines = block.split('\n')

    # Check code block (start and end with ``` exactly)
    if lines[0].startswith("```") and lines[-1].endswith("```") and len(lines) >= 2:
        return BlockType.CODE

    # Check heading (# followed by space)
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    # Check quote (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Check unordered list (every line starts with "- ")
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Check ordered list (lines start with "1. ", "2. ", "3. ", ...)
    if all(re.match(r"^\d+\. ", line) for line in lines):
        expected_number = 1
        for line in lines:
            match = re.match(r"^(\d+)\. ", line)
            if not match or int(match.group(1)) != expected_number:
                return BlockType.PARAGRAPH
            expected_number += 1
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH

from htmlnode import ParentNode, LeafNode
from markdown_splitters import (
    split_nodes_bold,
    split_nodes_italic,
    split_nodes_code,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextType, TextNode
from conversions import text_node_to_html_node, markdown_to_blocks, block_to_block_type, BlockType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for splitter in [
        split_nodes_image,
        split_nodes_link,
        split_nodes_bold,
        split_nodes_italic,
        split_nodes_code,
    ]:
        nodes = splitter(nodes)
    return nodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_to_html(block):
    return ParentNode("p", text_to_children(block))

def heading_to_html(block):
    level = len(block.split(" ")[0])  # Count #
    text = block[level + 1:]  # Skip '# ' at beginning
    return ParentNode(f"h{level}", text_to_children(text))

def code_to_html(block):
    content = "\n".join(block.split("\n")[1:-1]) + "\n"  # Drop ``` lines
    return ParentNode("pre", [LeafNode("code", content)])

def quote_to_html(block):
    cleaned = "\n".join([line[1:].lstrip() for line in block.split("\n")])
    return ParentNode("blockquote", text_to_children(cleaned))

def unordered_list_to_html(block):
    items = block.split("\n")
    children = [ParentNode("li", text_to_children(item[2:])) for item in items]
    return ParentNode("ul", children)

def ordered_list_to_html(block):
    items = block.split("\n")
    children = [ParentNode("li", text_to_children(item[item.find('.') + 2:])) for item in items]
    return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            children.append(heading_to_html(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html(block))
        elif block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html(block))

    return ParentNode("div", children)
