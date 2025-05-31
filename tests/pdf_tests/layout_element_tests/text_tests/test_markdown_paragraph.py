import unittest

from borb.pdf import Document, Page, PDF, Lipsum, X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.markdown_paragraph import MarkdownParagraph


class TestMarkdownParagraph(unittest.TestCase):

    def test_markdown_paragraph(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        MarkdownParagraph(
            """
        Experiamur igitur inquit vitae *beatum* et quasi *dilatari putant*. 
        Ex rebus humanis ut tibi _serviremus aliud negotii_ nihil habemus.
        Itaque eos quos eduxerat **Sparta** cum esset ~proposita aut inminuta~ sint occultent homines? 
        Ex rebus enim illam ~~non tam haesitaret~~.
        """,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_markdown_paragraph.pdf")

    def test_markdown_paragraph_eliminates_space(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        MarkdownParagraph(
            """
        Experiamur igitur inquit vitae *beatum* et quasi *dilatari putant*. 
        Ex rebus humanis ut tibi _serviremus aliud negotii_ nihil habemus.
        Itaque eos quos eduxerat **Sparta** cum esset ~proposita aut inminuta~ sint occultent homines? 
        Ex rebus enim illam ~~non tam haesitaret~~.
        """.replace(
                " ", " " * 3
            ),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_markdown_paragraph_eliminates_space.pdf"
        )

    def test_markdown_paragraph_respects_escaped_chars(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        MarkdownParagraph(
            """
        Experiamur igitur inquit vitae \*beatum\* et quasi *dilatari putant*. 
        Ex rebus humanis ut tibi _serviremus aliud negotii_ nihil habemus.
        Itaque eos quos eduxerat **Sparta** cum esset ~proposita aut inminuta~ sint occultent homines? 
        Ex rebus enim illam ~~non tam haesitaret~~.
        """.replace(
                " ", " " * 3
            ),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_markdown_paragraph_respects_escaped_chars.pdf"
        )
