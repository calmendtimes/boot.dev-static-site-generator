from typing import Any


class HTMLNode:

    def __init__(self, tag:str=None, value:Any=None, children:list=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props: return ""
        return " " + " ".join([f"{k}=\"{v}\"" for k,v in self.props.items()]) + " "

    def __repr__(self):
        return f"tag:{self.tag}\nvalue:{self.value}\nchildren:{self.children}\nprops:{self.props_to_html()}"