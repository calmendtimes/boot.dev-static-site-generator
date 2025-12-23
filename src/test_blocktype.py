import unittest

import blocktype


class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = [
            "This is **bolded** paragraph",
            "text in a p",
            "tag here",
            "",
            "This is another paragraph with _italic_ text and `code` here" ]
        
        md = "\n".join(md)
        node = blocktype.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = [
            "- This is a list",
            "- with items",
            "- and _more_ items",
            "",
            "1. This is an `ordered` list",
            "2. with items",
            "3. and more items"]

        md = "\n".join(md)
        node = blocktype.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = [
            "# this is an h1",
            "",
            "this is paragraph text",
            "",
            "## this is an h2"]
        md = "\n".join(md)
        node = blocktype.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = [
            "> This is a",
            "> blockquote block",
            "",
            "this is paragraph text",
            ""]
        md = "\n".join(md)
        node = blocktype.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_codeblock(self):
        md = [
            "```",
            "This is text that _should_ remain",
            "the **same** even with inline stuff",
            "```"]
        md = "\n".join(md)
        node = blocktype.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = [
            "This is **bolded** paragraph",
            "",
            "This is another paragraph with _italic_ text and `code` here",
            "This is the same paragraph on a new line",
            "",
            "- This is a list",
            "- with items"]
        md = "\n".join(md)
        blocks = blocktype.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class Test_block_to_block_type(unittest.TestCase):
    def test_block_to_block_type(self):
        md = [
            "paragraph",
            "",
            "### Header",
            "continuation of header paragraph",
            "",
            "``` code",
            "    block",
            "?```",
            "",
            "> quote",
            "> quote quote",
            "",
            "- unordered list 1",
            "- 2",
            "- 3",
            "",
            "1. ordered list 1",
            "2. 2",
            "3. 3",
            "",
            "9. just paragraph",
            "8. continuation",
            "7. of paragraph",
            "> yes"]
        md = "\n".join(md)
        blocks = blocktype.markdown_to_blocks(md)
        types = [blocktype.block_to_block_type(b) for b in blocks]
        expected = [
            blocktype.BlockType.paragraph, 
            blocktype.BlockType.heading, 
            blocktype.BlockType.code, 
            blocktype.BlockType.quote, 
            blocktype.BlockType.unordered_list, 
            blocktype.BlockType.ordered_list, 
            blocktype.BlockType.paragraph
        ]
        self.assertEqual(expected, types)


class Test_extract_title(unittest.TestCase):
    def test_extracts_title(self):
        md = [
            "### h3",
            "",
            "## h2",
            "",
            "# h1 heading",
            "asdfasdf"
            ""]
        md = "\n".join(md)
        heading = blocktype.extract_title(md)
        self.assertEqual( heading, "h1 heading" )

    def test_throws_when_no_heading_found(self):
        md = [
            "### h3",
            "",
            "## h2",
            ""]
        md = "\n".join(md)
        with self.assertRaises(Exception):
            blocktype.extract_title(md)
