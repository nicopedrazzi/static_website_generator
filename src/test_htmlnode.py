import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        result = node.props_to_html()
        self.assertTrue(result.startswith(" "))
        self.assertIn(' href="https://www.google.com" target="_blank"', result)
        
    def test_props_to_html_none_props_returns_empty_string(self):
        node = HTMLNode(tag="p", value="hello", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict_returns_empty_string(self):
        node = HTMLNode(tag="p", value="hello", props={})
        self.assertEqual(node.props_to_html(), "")
    

if __name__ == "__main__":
    unittest.main()

