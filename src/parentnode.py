from typing import Any
from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag:str, children:list, props:dict=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag: raise ValueError("Parent node must have a tag.")
        if not self.children: raise ValueError("Parent node must have children")

        children_html = ""
        for c in self.children:
            children_html += c.to_html()

        result_html = f"<{self.tag}{super().props_to_html()}>{children_html}</{self.tag}>"
        return result_html