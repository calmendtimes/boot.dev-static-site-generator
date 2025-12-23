import re
from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
import textnode


class BlockType(Enum):
    paragraph       = "paragraph"
    heading         = "heading"
    code            = "code"
    quote           = "quote"
    unordered_list  = "unordered_list"
    ordered_list    = "ordered_list"



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = None

        match block_type:
            case BlockType.paragraph:       html_node = paragraph_to_html(block)
            case BlockType.heading:         html_node = heading_to_html(block)      
            case BlockType.code:            html_node = code_to_html(block)
            case BlockType.quote:           html_node = quote_to_html(block)          
            case BlockType.unordered_list:  html_node = unordered_list_to_html(block)
            case BlockType.ordered_list:    html_node = ordered_list_to_html(block)
        
        html_nodes.append(html_node)


    div = ParentNode("div", html_nodes)
    return div
                   


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks]
    blocks = [b for b in blocks if b]
    return blocks


def block_to_block_type(block):
    if len(re.findall(r"^#{1,6} ", block)) == 1: 
        return BlockType.heading

    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.code
    
    if all(l[0]==">" for l in block.split("\n")):
        return BlockType.quote
    
    if all(l[0:2]=="- " for l in block.split("\n")):
        return BlockType.unordered_list
    
    lines = [l for l in block.split("\n")]
    matches = [re.search(r"^\d+\.", l) for l in lines]
    if all(matches):
        try:
            numbers = [int(m.group()[:-1]) for m in matches]
            if list(range(1,len(lines)+1)) == numbers:
                return BlockType.ordered_list
        except Exception as e:
            pass
    
    return BlockType.paragraph   



def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for b in blocks:
        block_type = block_to_block_type(b)
        if block_type == BlockType.heading:
            if b[0:2] == "# ":
                return b.split("\n")[0][2:]
    raise Exception("No heading '# ' found.")


def paragraph_to_html(block):
    block = block.replace("\n", " ")
    text_nodes = textnode.text_to_textnodes(block)     
    html_nodes = [textnode.text_node_to_html_node(tn) for tn in text_nodes]
    html_node = ParentNode("p", html_nodes)
    return html_node


def heading_to_html(block):
    heading_prefix_match = re.findall(r"^#{1,6} ", block)[0]
    heading_level = len(heading_prefix_match) - 1
    text_nodes = textnode.text_to_textnodes(block[heading_level+1:])   
    html_nodes = [textnode.text_node_to_html_node(tn) for tn in text_nodes]
    html_node = ParentNode(f"h{heading_level}", html_nodes)
    return html_node


def code_to_html(block):
    code = block[3:-3]
    code_ln = LeafNode("code", code)
    html_node = ParentNode("pre", [code_ln])
    return html_node


def quote_to_html(block):
    lines = block.split("\n")
    lines = [l[1:] for l in lines]
    text = "".join(lines)
    text = text.strip()
    text_nodes = textnode.text_to_textnodes(text)  
    html_nodes = [textnode.text_node_to_html_node(tn) for tn in text_nodes]
    html_node = ParentNode("blockquote", html_nodes)
    return html_node


def unordered_list_to_html(block):
    lines = block.split("\n")
    lines = [l[2:] for l in lines]
    html_nodes = []

    for l in lines:
        line_text_nodes = textnode.text_to_textnodes(l)
        line_html_nodes = [textnode.text_node_to_html_node(tn) for tn in line_text_nodes]
        html_node = ParentNode("li", line_html_nodes)
        html_nodes.append(html_node)

    html_node = ParentNode("ul", html_nodes)
    return html_node


def ordered_list_to_html(block):
    lines = [l for l in block.split("\n")]
    matches = [re.search(r"^(\d+\.)(.*)", l) for l in lines]
    numbers = [int(m[1][:-1]) for m in matches]
    lines = [m[2].strip() for m in matches]
    html_nodes = []

    for l in lines:
        line_text_nodes = textnode.text_to_textnodes(l)
        line_html_nodes = [textnode.text_node_to_html_node(tn) for tn in line_text_nodes]
        html_node = ParentNode("li", line_html_nodes)
        html_nodes.append(html_node)

    html_node = ParentNode("ol", html_nodes)
    return html_node