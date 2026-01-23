from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain_text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None, children=None):
        self.text = text
        self.text_type = text_type
        self.url = url 
        self.children = children

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url and self.children==other.children:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}, {self.children})"
    

