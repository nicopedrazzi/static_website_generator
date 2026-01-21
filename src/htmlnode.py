


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

