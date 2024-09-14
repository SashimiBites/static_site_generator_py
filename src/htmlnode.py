class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML node should have a tag")

        if self.children is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        children_text = ""
        for child in self.children:
            children_text += child.to_html()

        return f"<{self.tag}>{children_text}</{self.tag}>"

    def props_to_html(self):
        if self.props is None:
            return ""

        html_props = ""
        for prop in self.props:
            html_props += f'{prop}="{self.props[prop]}" '

        return html_props[:-1]

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
