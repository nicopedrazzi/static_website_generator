from warnings import warn
from textnode import TextType, TextNode
import re
from htmlnode import LeafNode 
##add the function from the other file as it will be more organized to have it here
#this one can become nested, let's see in the future

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN_TEXT:
        return LeafNode(tag = None, value = text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value = text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i",value = text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value= text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value = text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value = "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Unknown Type")
  


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter: {delimiter}")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        parts = extract_markdown_images(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        image_alt, image_link = parts[0]

        before, after = node.text.split(f"![{image_alt}]({image_link})", 1)

        if before:
            new_nodes.append(TextNode(before, TextType.PLAIN_TEXT))
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))

        if after:
            new_nodes.extend(split_nodes_images([TextNode(after, TextType.PLAIN_TEXT)]))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        parts = extract_markdown_links(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        links_text, link = parts[0]

        before, after = node.text.split(f"[{links_text}]({link})", 1)

        if before:
            new_nodes.append(TextNode(before, TextType.PLAIN_TEXT))
        new_nodes.append(TextNode(links_text, TextType.LINK, url=link))

        if after:
            new_nodes.extend(split_nodes_links([TextNode(after, TextType.PLAIN_TEXT)]))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    return nodes

def markdown_to_blocks(markdown):
    split = markdown.split("\n\n")
    blocks = []
    for block in split:
        block = block.strip()
        if not block:
            continue
        blocks.append(block)
    return blocks


