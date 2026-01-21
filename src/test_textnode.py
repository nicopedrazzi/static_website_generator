import unittest

from textnode import TextNode, TextType



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


if __name__ == "__main__":
    unittest.main()

