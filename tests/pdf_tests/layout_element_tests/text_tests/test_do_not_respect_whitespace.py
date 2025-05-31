import unittest
from borb.pdf import (
    Document,
    Page,
    PageLayout,
    X11Color,
    HeterogeneousParagraph,
    Chunk,
    PDF,
    SingleColumnLayout,
)


class TestDoNotRespectWhitespace(unittest.TestCase):

    def test_do_not_respect_infix_whitespace(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: PageLayout = SingleColumnLayout(page)

        # ground truth
        layout.append_layout_element(
            HeterogeneousParagraph(
                chunks=[Chunk("Lorem Ipsum Dolor Sit Amet")],
                border_color=X11Color.GREEN,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
            )
        )

        # increasing number of leading whitespace(s)
        for i in range(1, 10):
            layout.append_layout_element(
                HeterogeneousParagraph(
                    chunks=[
                        Chunk("Lorem Ipsum "),
                        Chunk(" " * i),
                        Chunk("Dolor Sit Amet"),
                    ],
                    border_color=X11Color.RED,
                    border_width_top=1,
                    border_width_right=1,
                    border_width_bottom=1,
                    border_width_left=1,
                )
            )

        # store
        PDF.write(what=doc, where_to="assets/test_do_not_respect_infix_whitespace.pdf")

    def test_do_not_respect_leading_whitespace(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: PageLayout = SingleColumnLayout(page)

        # ground truth
        layout.append_layout_element(
            HeterogeneousParagraph(
                chunks=[Chunk("Lorem Ipsum Dolor Sit Amet")],
                border_color=X11Color.GREEN,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
            )
        )

        # increasing number of leading whitespace(s)
        for i in range(1, 10):
            layout.append_layout_element(
                HeterogeneousParagraph(
                    chunks=[Chunk(" " * i), Chunk("Lorem Ipsum Dolor Sit Amet")],
                    border_color=X11Color.RED,
                    border_width_top=1,
                    border_width_right=1,
                    border_width_bottom=1,
                    border_width_left=1,
                )
            )

        # store
        PDF.write(
            what=doc, where_to="assets/test_do_not_respect_leading_whitespace.pdf"
        )

    def test_do_not_respect_trailing_whitespace(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: PageLayout = SingleColumnLayout(page)

        # ground truth
        layout.append_layout_element(
            HeterogeneousParagraph(
                chunks=[Chunk("Lorem Ipsum Dolor Sit Amet")],
                border_color=X11Color.GREEN,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
            )
        )

        # increasing number of leading whitespace(s)
        for i in range(1, 10):
            layout.append_layout_element(
                HeterogeneousParagraph(
                    chunks=[Chunk("Lorem Ipsum Dolor Sit Amet"), Chunk(" " * i)],
                    border_color=X11Color.RED,
                    border_width_top=1,
                    border_width_right=1,
                    border_width_bottom=1,
                    border_width_left=1,
                )
            )

        # store
        PDF.write(
            what=doc, where_to="assets/test_do_not_respect_trailing_whitespace.pdf"
        )
