class HTMLNode:
    def to_html(self, basepath="/"):
        raise NotImplementedError()

    def props_to_html(self):
        if not hasattr(self, "props") or not self.props:
            return ""
        props = []
        for key, val in self.props.items():
            props.append(f'{key}="{val}"')
        return " " + " ".join(props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        self.tag = tag
        self.value = value
        self.props = props or {}

    def to_html(self, basepath="/"):
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()

        # Fix src and href paths with basepath
        if self.tag == "img" and "src" in self.props:
            self.props["src"] = basepath + self.props["src"].lstrip("/")
        if self.tag == "a" and "href" in self.props and self.props["href"].startswith("/"):
            self.props["href"] = basepath + self.props["href"].lstrip("/")

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        self.tag = tag
        self.children = children or []
        self.props = props or {}

    def to_html(self, basepath="/"):
        children_html = "".join(child.to_html(basepath=basepath) for child in self.children)
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
