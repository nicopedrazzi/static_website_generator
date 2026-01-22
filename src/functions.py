from textnode import TextType, TextNode
import re
from htmlnode import LeafNode, HTMLNode, ParentNode
from blocknode import BlockType

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
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

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


def block_to_block_type(block):
    lines = block.split("\n")

    if lines[0].startswith("#"):
        i = 0
        while i < len(lines[0]) and lines[0][i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(lines[0]) and lines[0][i] == " ":
            return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    expected = 1
    for line in lines:
        if not line.startswith(f"{expected}. "):
            break
        expected += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text) 
    return [text_node_to_html_node(tn) for tn in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            lines = [line.strip() for line in block.splitlines()]
            text = " ".join(line for line in lines if line)
            children.append(ParentNode("p", text_to_children(text)))

        elif btype == BlockType.HEADING:
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1
            text = block[level:].lstrip()
            children.append(ParentNode(f"h{level}", text_to_children(text)))

        elif btype == BlockType.QUOTE:
            lines = block.splitlines()
            stripped = [line[1:].lstrip() for line in lines]
            text = "\n".join(stripped)
            children.append(ParentNode("blockquote", text_to_children(text)))

        elif btype == BlockType.UNORDERED_LIST:
            items = []
            for line in block.splitlines():
                item_text = line[1:].strip()
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ul", items))

        elif btype == BlockType.ORDERED_LIST:
            items = []
            for line in block.splitlines():
                dot = line.find(".")
                item_text = line[dot + 1 :].strip()
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(children("ol", items))

        elif btype == BlockType.CODE:
            lines = block.splitlines()
            code_lines = lines[1:-1]
            non_empty = [line for line in code_lines if line.strip()]
            min_indent = min(
                (len(line) - len(line.lstrip()) for line in non_empty),
                default=0,
            )
            trimmed_lines = [line[min_indent:] for line in code_lines]
            inner = "\n".join(trimmed_lines) + "\n"
            code_text = TextNode(inner, TextType.PLAIN_TEXT)
            code_child = text_node_to_html_node(code_text)
            code_node = ParentNode("code", [code_child])
            children.append(ParentNode("pre", [code_node]))

        else:
            raise ValueError(f"Unknown block type: {btype}")

    return ParentNode("div", children)
