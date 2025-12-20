import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        node1 = LeafNode("tag_1", "value_1", { "prop_1":111, "prop_2":222 })
        html1 = node1.to_html()
        expect = "<tag_1 prop_1=\"111\" prop_2=\"222\" >value_1</tag_1>"
        self.assertEqual(html1, expect)

    def test_to_html_no_value_exception(self):
        with self.assertRaises(ValueError):
            node1 = LeafNode("tag_1", None, { "prop_1":111, "prop_2":222 })
            node1.to_html()
    


if __name__ == "__main__":
    unittest.main()