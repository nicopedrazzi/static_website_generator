import unittest
from src.htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
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

    def test_to_html_multiple_children_mixed_tags(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_many_children(self):
        children = [LeafNode("span", str(i)) for i in range(5)]
        node = ParentNode("div", children)
        self.assertEqual(
            node.to_html(),
            "<div><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span></div>",
        )

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "hi"),
                                LeafNode("b", "there"),
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p>hi<b>there</b></p></section></div>",
        )

    def test_to_html_empty_children_list_allowed(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_missing_tag_raises(self):
        node = ParentNode(None, [LeafNode(None, "x")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_string_tag_raises(self):
        node = ParentNode("", [LeafNode(None, "x")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_children_is_none_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_nested_parent_siblings(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "a")]),
                ParentNode("p", [LeafNode(None, "b")]),
            ],
        )
        self.assertEqual(node.to_html(), "<div><p>a</p><p>b</p></div>")

    def test_parent_with_props_does_not_break(self):
      
        node = ParentNode("div", [LeafNode(None, "x")], props={"class": "container"})
        html = node.to_html()
        self.assertIn(">x</div>", html)
        self.assertTrue(html.startswith("<div"))

    def test_recursion_with_mixed_levels(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "one")]),
                ParentNode("li", [LeafNode(None, "two")]),
                ParentNode("li", [ParentNode("span", [LeafNode(None, "three")])]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li>one</li><li>two</li><li><span>three</span></li></ul>",
        )


if __name__ == "__main__":
    unittest.main()

