from textnode import TextNode, TextType
from markdown_extractors import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            split_str = f"![{alt}]({url})"
            before, after = text.split(split_str, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for anchor, url in links:
            split_str = f"[{anchor}]({url})"
            before, after = text.split(split_str, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

import re
from textnode import TextNode, TextType

def split_nodes_bold(old_nodes):
    pattern = r"\*\*([^\*]+)\*\*"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(pattern, text):
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
            new_nodes.append(TextNode(match.group(1), TextType.BOLD))
            last_index = end
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes

def split_nodes_italic(old_nodes):
    pattern = r"_(.+?)_"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(pattern, text):
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
            new_nodes.append(TextNode(match.group(1), TextType.ITALIC))
            last_index = end
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes

def split_nodes_code(old_nodes):
    pattern = r"`([^`]+)`"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        last_index = 0
        for match in re.finditer(pattern, text):
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
            new_nodes.append(TextNode(match.group(1), TextType.CODE))
            last_index = end
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes

