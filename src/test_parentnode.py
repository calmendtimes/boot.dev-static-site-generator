import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    # def test_to_html(self):
    #     node1 = LeafNode("tag_1", [], { "prop_1":111, "prop_2":222 })
    #     html1 = node1.to_html()
    #     expect = "<tag_1 prop_1=\"111\" prop_2=\"222\" >value_1</tag_1>"
    #     self.assertEqual(html1, expect)

    def test_to_html_no_tag_exception(self):
        with self.assertRaises(ValueError):
            node1 = ParentNode("", ["child_1"], { "prop_1":111, "prop_2":222 })
            node1.to_html()
    
    def test_to_html_no_children_exception(self):
        with self.assertRaises(ValueError):
            node1 = ParentNode("tag_1", [], { "prop_1":111, "prop_2":222 })
            node1.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild", { "prop_gc":"GC GC GC" })
        child_node = ParentNode("span", [grandchild_node], { "prop_c":"CCC" })
        parent_node = ParentNode("div", [child_node], { "prop_1":"111" })
        self.assertEqual(
            parent_node.to_html(),
            "<div prop_1=\"111\" ><span prop_c=\"CCC\" ><b prop_gc=\"GC GC GC\" >grandchild</b></span></div>",
        )




if __name__ == "__main__":
    unittest.main()