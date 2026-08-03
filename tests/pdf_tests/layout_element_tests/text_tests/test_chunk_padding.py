from borb.pdf import Document, Page, PageLayout, Chunk, X11Color, SingleColumnLayout
from tests.test_case import TestCase


class TestChunkPadding(TestCase):

    def test_chunk_padding_left_100(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                padding_left=100,
            )
        )

        TestCase.write(what=d, where_to="test_chunk_padding_left_100.pdf")

    def test_chunk_padding_left_200(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                padding_left=200,
            )
        )

        TestCase.write(what=d, where_to="test_chunk_padding_left_200.pdf")
