from textnode import TextType


class HTMLNode:
    def __init__(self,tag = None,value=None,children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props:
            return ""
        parts = []
        for key,value in self.props.items():
            parts.append(f'{key}="{value}"')
        return " " + " ".join(parts)
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
 
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag,value=value,children=None,props=props)
        
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        else:
            converted = self.props_to_html()
            return f"<{self.tag}{converted}>{self.value}</{self.tag}>"

    def __repr__(self):
         return f"HTMLNode({self.tag},{self.value},{self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        if self.children is None:
            raise ValueError("missing children")

        inner = "".join(child.to_html() for child in self.children)
        props_html = self.props_to_html() if self.props else ""
        return f"<{self.tag}{props_html}>{inner}</{self.tag}>"


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
  
  

