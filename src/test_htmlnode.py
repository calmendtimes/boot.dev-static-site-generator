import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # def test_eq(self):
    #     node1 = HTMLNode("tag 1", "Value 1", ["child 1", "child 2"], { "prop_1":111, "prop_2":222 })
    #     node2 = HTMLNode("tag 1", "Value 1", ["child 1", "child 2"], { "prop_1":111, "prop_2":222 })
    #     self.assertEqual(node1, node2)

    def test_props_to_html(self):
        node1 = HTMLNode("tag 1", "Value 1", ["child 1", "child 2"], { "prop_1":111, "prop_2":222 })
        html1 = node1.props_to_html()
        expect = " prop_1=\"111\" prop_2=\"222\" "
        self.assertEqual(html1, expect)


if __name__ == "__main__":
    unittest.main()