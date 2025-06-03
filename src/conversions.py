from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from markdown_splitters import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_bold,
    split_nodes_italic,
    split_nodes_code,
)
import re
from enum import Enum, auto

def text_node_to_html_node(text_node, basepath=""):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        href = text_node.url
        if href.startswith("/"):
            href = basepath.rstrip("/") + href
        return LeafNode("a", text_node.text, {"href": href})
    elif text_node.text_type == TextType.IMAGE:
        src = text_node.url
        if src.startswith("/"):
            src = basepath.rstrip("/") + src
        return LeafNode("img", "", {"src": src, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")

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

def text_to_children(text, basepath=""):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node, basepath) for node in text_nodes]

def paragraph_to_html(block, basepath=""):
    return ParentNode("p", text_to_children(block, basepath))

def heading_to_html(block, basepath=""):
    level = len(block.split(" ")[0])
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text, basepath))

def code_to_html(block):
    content = "\n".join(block.split("\n")[1:-1]) + "\n"
    return ParentNode("pre", [LeafNode("code", content)])

def quote_to_html(block, basepath=""):
    cleaned = "\n".join([line[1:].lstrip() for line in block.split("\n")])
    return ParentNode("blockquote", text_to_children(cleaned, basepath))

def unordered_list_to_html(block, basepath=""):
    items = block.split("\n")
    children = [ParentNode("li", text_to_children(item[2:], basepath)) for item in items]
    return ParentNode("ul", children)

def ordered_list_to_html(block, basepath=""):
    items = block.split("\n")
    children = [ParentNode("li", text_to_children(item[item.find('.') + 2:], basepath)) for item in items]
    return ParentNode("ol", children)

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in raw_blocks if block.strip() != '']
    return blocks

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def block_to_block_type(block):
    lines = block.split('\n')
    if lines[0].startswith("```") and lines[-1].endswith("```") and len(lines) >= 2:
        return BlockType.CODE
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(r"^\d+\. ", line) for line in lines):
        expected_number = 1
        for line in lines:
            match = re.match(r"^(\d+)\. ", line)
            if not match or int(match.group(1)) != expected_number:
                return BlockType.PARAGRAPH
            expected_number += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown, basepath=""):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(heading_to_html(block, basepath))
        elif block_type == BlockType.CODE:
            children.append(code_to_html(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html(block, basepath))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html(block, basepath))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html(block, basepath))
        elif block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html(block, basepath))
    return ParentNode("div", children)
