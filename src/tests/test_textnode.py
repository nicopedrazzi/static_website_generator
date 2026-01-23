import unittest

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode
from src.functions import *


class TestTextNode(unittest.TestCase):
    def test_eq_same_props(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url_none_vs_url_set(self):
        node1 = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, url="fake/url")
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_urls(self):
        node1 = TextNode("This is a text node", TextType.LINK, url="a")
        node2 = TextNode("This is a text node", TextType.LINK, url="b")
        self.assertNotEqual(node1, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("alt text here", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/img.png", "alt": "alt text here"},
        )

    def test_unknown_type_raises(self):
        class FakeType:
            pass

        node = TextNode("oops", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_code_delimiter_single_pair(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

  
    def test_split_italic_delimiter_basic(self):
        node = TextNode("A _little_ italic here", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("A ", TextType.PLAIN_TEXT),
            TextNode("little", TextType.ITALIC),
            TextNode(" italic here", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_plain_text_nodes_are_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is `broken code", TextType.PLAIN_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    
    def test_split_nodes_images_single_image_middle(self):
        node = TextNode(
            "Start ![alt](https://example.com/a.png) end",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("Start ", TextType.PLAIN_TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" end", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_images_image_at_start(self):
        node = TextNode(
            "![alt](https://example.com/a.png) tail",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" tail", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_images_image_at_end(self):
        node = TextNode(
            "Head ![alt](https://example.com/a.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("Head ", TextType.PLAIN_TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_images_multiple_images(self):
        node = TextNode(
            "A ![one](https://example.com/1.png) B ![two](https://example.com/2.png) C",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_images([node])
        expected = [
            TextNode("A ", TextType.PLAIN_TEXT),
            TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" B ", TextType.PLAIN_TEXT),
            TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(" C", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_images_no_images_returns_original(self):
        node = TextNode("Just plain text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_images_non_plain_text_unchanged(self):
        node = TextNode(
            "![alt](https://example.com/a.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_images_multiple_nodes_mixed(self):
        nodes = [
            TextNode("First ![a](https://example.com/a.png) node", TextType.PLAIN_TEXT),
            TextNode("Already code", TextType.CODE),
            TextNode("Second ![b](https://example.com/b.png)", TextType.PLAIN_TEXT),
        ]
        new_nodes = split_nodes_images(nodes)
        expected = [
            TextNode("First ", TextType.PLAIN_TEXT),
            TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" node", TextType.PLAIN_TEXT),
            TextNode("Already code", TextType.CODE),
            TextNode("Second ", TextType.PLAIN_TEXT),
            TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
        ]
        self.assertEqual(new_nodes, expected)
    def test_split_nodes_links_single_link_middle(self):
        node = TextNode(
        "Go to [Boot.dev](https://www.boot.dev) now",
        TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_links([node])
        expected = [
        TextNode("Go to ", TextType.PLAIN_TEXT),
        TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" now", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)


    def test_split_nodes_links_multiple_links(self):
        node = TextNode(
            "Links: [one](https://example.com/1) and [two](https://example.com/2).",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_links([node])
        expected = [
            TextNode("Links: ", TextType.PLAIN_TEXT),
            TextNode("one", TextType.LINK, "https://example.com/1"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("two", TextType.LINK, "https://example.com/2"),
            TextNode(".", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)


    def test_text_to_textnodes_plain_text_only(self):
        text = "Just plain text."
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text.", TextType.PLAIN_TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_bold_italic_code(self):
        text = "A **bold** and *italic* and `code`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("A ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_link_and_image(self):
        text = "See ![alt](https://example.com/a.png) and [site](https://example.com)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.PLAIN_TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("site", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_code_suppresses_formatting_inside(self):
        text = "`**not bold** and *not italic*` outside"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("**not bold** and *not italic*", TextType.CODE),
            TextNode(" outside", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_multiple_images_and_links(self):
        text = "A ![one](u1) B [two](u2) C ![three](u3) D [four](u4)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("A ", TextType.PLAIN_TEXT),
            TextNode("one", TextType.IMAGE, "u1"),
            TextNode(" B ", TextType.PLAIN_TEXT),
            TextNode("two", TextType.LINK, "u2"),
            TextNode(" C ", TextType.PLAIN_TEXT),
            TextNode("three", TextType.IMAGE, "u3"),
            TextNode(" D ", TextType.PLAIN_TEXT),
            TextNode("four", TextType.LINK, "u4"),
        ]
        self.assertEqual(nodes, expected)

    def test_multiple_blank_lines_between_blocks(self):
        markdown = "Block 1\n\n\n\nBlock 2"
        self.assertEqual(markdown_to_blocks(markdown), ["Block 1", "Block 2"])

    def test_leading_and_trailing_blank_lines_in_whole_markdown(self):
        markdown = "\n\nBlock 1\n\nBlock 2\n\n"
        self.assertEqual(markdown_to_blocks(markdown), ["Block 1", "Block 2"])

    def test_blocks_can_contain_multiple_lines(self):
        markdown = "Line 1\nLine 2\nLine 3\n\nAnother 1\nAnother 2"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["Line 1\nLine 2\nLine 3", "Another 1\nAnother 2"],
        )
    def test_block_to_block_type_heading(self):
        block = "### Hello world"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_ordered_list_requires_incrementing(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()

