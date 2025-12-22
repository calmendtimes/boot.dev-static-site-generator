import re
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

    def __init__(self, text:str, text_type:TextType, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold_text)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic_text)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code_text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_node_to_html_node(text_node:TextNode):
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


  
def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
    new_nodes = []

    for n in old_nodes:
        if n.text_type != TextType.text:
            new_nodes.append(n)
        else:
            split = n.text.split(delimiter)
            if len(split) % 2 == 0: raise ValueError("Invalid markdown.")
            for i in range(len(split)):
                p = split[i]
                if p == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(p, TextType.text))
                else:
                    new_nodes.append(TextNode(p, text_type))
    
    return new_nodes
                

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        matches = extract_markdown_images(n.text)
        if not matches:
            new_nodes.append(n)
        text = n.text
        for m in matches:
            img = f"![{m[0]}]({m[1]})"
            s = text.split(img)
            text = s[1]
            new_nodes.append(TextNode(s[0], TextType.text))
            new_nodes.append(TextNode(m[0], TextType.image, m[1]))
            if m == matches[-1] and s[1] != "":
                new_nodes.append(TextNode(s[1], TextType.text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        matches = extract_markdown_links(n.text)
        if not matches:
            new_nodes.append(n)
        text = n.text
        for m in matches:
            link = f"[{m[0]}]({m[1]})"
            s = text.split(link)
            text = s[1]
            new_nodes.append(TextNode(s[0], TextType.text))
            new_nodes.append(TextNode(m[0], TextType.link, m[1]))
            if m == matches[-1] and s[1] != "": 
                new_nodes.append(TextNode(s[1], TextType.text))
    return new_nodes
