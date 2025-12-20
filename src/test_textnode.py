import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.bold_text)
        node2 = TextNode("This is a text node", TextType.bold_text)
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("text 1", TextType.text)
        node2 = TextNode("text 2", TextType.text)
        self.assertNotEqual(node1, node2)

    def test_not_eq_text_type(self):
        node1 = TextNode("text", TextType.italic_text)
        node2 = TextNode("text", TextType.bold_text)
        self.assertNotEqual(node1, node2)
    
    def test_not_eq_url(self):
        node1 = TextNode("text", TextType.text, "url 1")
        node2 = TextNode("text", TextType.text, "url 2")
        self.assertNotEqual(node1, node2)
        

class Test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.bold_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic_text(self):
        node = TextNode("This is a text node", TextType.italic_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code_text(self):
        node = TextNode("This is a text node", TextType.code_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link_text(self):
        node = TextNode("This is a text node", TextType.link, "url_1")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), "<a href=\"url_1\" >This is a text node</a>")

    def test_image_text(self):
        node = TextNode("alt_1", TextType.image, "url_1")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "<img src=\"url_1\" alt=\"alt_1\" ></img>")



if __name__ == "__main__":
    unittest.main()