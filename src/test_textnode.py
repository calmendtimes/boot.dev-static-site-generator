import unittest

from textnode import TextNode, TextType
import textnode


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
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.bold_text)
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic_text(self):
        node = TextNode("This is a text node", TextType.italic_text)
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code_text(self):
        node = TextNode("This is a text node", TextType.code_text)
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link_text(self):
        node = TextNode("This is a text node", TextType.link, "url_1")
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), "<a href=\"url_1\" >This is a text node</a>")

    def test_image_text(self):
        node = TextNode("alt_1", TextType.image, "url_1")
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "<img src=\"url_1\" alt=\"alt_1\" ></img>")


class Test_split_nodes_delimiter(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.text)
        new_nodes = textnode.split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("bolded", TextType.bold_text),
                TextNode(" word", TextType.text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.text
        )
        new_nodes = textnode.split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("bolded", TextType.bold_text),
                TextNode(" word and ", TextType.text),
                TextNode("another", TextType.bold_text),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.text
        )
        new_nodes = textnode.split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("bolded word", TextType.bold_text),
                TextNode(" and ", TextType.text),
                TextNode("another", TextType.bold_text),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.text)
        new_nodes = textnode.split_nodes_delimiter([node], "_", TextType.italic_text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("italic", TextType.italic_text),
                TextNode(" word", TextType.text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.text)
        new_nodes = textnode.split_nodes_delimiter([node], "**", TextType.bold_text)
        new_nodes = textnode.split_nodes_delimiter(new_nodes, "_", TextType.italic_text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.bold_text),
                TextNode(" and ", TextType.text),
                TextNode("italic", TextType.italic_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text)
        new_nodes = textnode.split_nodes_delimiter([node], "`", TextType.code_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("code block", TextType.code_text),
                TextNode(" word", TextType.text),
            ],
            new_nodes,
        )


class Test_extract_markdown_images(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = textnode.extract_markdown_images(
            "This is text with an ![image_1](link_1) and ![image_2](link_2) and NOT [image_?](link_?)")
        self.assertListEqual([("image_1", "link_1"), ("image_2", "link_2")], matches)


class Test_extract_markdown_links(unittest.TestCase):
    def test_extract_markdown_links(self):
        node = TextNode(
            "This is text with an [text_1](link_1) and [text_2](link_2) and NOT ![image_?](link_?)",
            TextType.text)
        new_nodes = textnode.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("text_1", TextType.link, "link_1"),
                TextNode(" and ", TextType.text),
                TextNode("text_2", TextType.link, "link_2"),
                TextNode(" and NOT ![image_?](link_?)", TextType.text),
            ],
            new_nodes,
        )


class Test_split_nodes_image(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image_1](link_1) and ![image_2](link_2) and NOT [image_?](link_?)",
            TextType.text)
        new_nodes = textnode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image_1", TextType.image, "link_1"),
                TextNode(" and ", TextType.text),
                TextNode("image_2", TextType.image, "link_2"),
                TextNode(" and NOT [image_?](link_?)", TextType.text),
            ],
            new_nodes,
        )


class Test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **bold text** with an _italic text_ and a `code block` and an ![image-1](link-1) and a [text-2](link-2)"
        expected = [
            TextNode("This is ", TextType.text),
            TextNode("bold text", TextType.bold_text),
            TextNode(" with an ", TextType.text),
            TextNode("italic text", TextType.italic_text),
            TextNode(" and a ", TextType.text),
            TextNode("code block", TextType.code_text),
            TextNode(" and an ", TextType.text),
            TextNode("image-1", TextType.image, "link-1"),
            TextNode(" and a ", TextType.text),
            TextNode("text-2", TextType.link, "link-2"),
        ]
        self.assertListEqual(expected, textnode.text_to_textnodes(text))



if __name__ == "__main__":
    unittest.main()