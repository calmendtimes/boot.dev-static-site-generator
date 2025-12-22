from typing import Any
from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag:str, value:Any, props:dict=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None: raise ValueError("Leaf node must have a value.")
        if not self.tag : return f"{self.value}"
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
        