from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode


class TextType(Enum):
    text        = "text"
    bold_text   = "bold_text"
    italic_text = "italic_text"
    code_text   = "code_text"
    link        = "link"
    image       = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.text:
            return LeafNode(None, text_node.text)
        case TextType.bold_text:
            return LeafNode("b", text_node.text)
        case TextType.italic_text:
            return LeafNode("i", text_node.text)
        case TextType.code_text:
            return LeafNode("code", text_node.text)
        case TextType.link:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.image:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Unrecognized type")

    
    # TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
    # TextType.BOLD: This should return a LeafNode with a "b" tag and the text
    # TextType.ITALIC: "i" tag, text
    # TextType.CODE: "code" tag, text
    # TextType.LINK: "a" tag, anchor text, and "href" prop
    # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props 
    #    ("src" is the image URL, "alt" is the alt text)