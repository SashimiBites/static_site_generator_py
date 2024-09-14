from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All lead nodes must have a value")

        if self.tag is None:
            return self.value

        props_string = ""
        if self.props is not None:
            props_string = " "
            props_string += self.props_to_html()

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
