from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node should have a tag")

        if self.children is None:
            raise ValueError("Parent node should have children")

        children_text = ""
        for child in self.children:
            children_text += child.to_html()

        return f"<{self.tag}>{children_text}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
