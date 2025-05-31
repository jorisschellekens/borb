import unittest

from borb.pdf import (
    Document,
    PageLayout,
    SingleColumnLayout,
    Page,
    Chunk,
    X11Color,
    PDF,
)


class TestChunkWordSpacing(unittest.TestCase):

    def test_chunk_word_spacing_00(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_00.pdf")

    def test_chunk_word_spacing_01(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.1,
            )
        )

    def test_chunk_word_spacing_02(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.2,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_02.pdf")

    def test_chunk_word_spacing_03(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.3,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_03.pdf")

    def test_chunk_word_spacing_04(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.4,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_04.pdf")

    def test_chunk_word_spacing_05(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.5,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_05.pdf")

    def test_chunk_word_spacing_06(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.6,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_06.pdf")

    def test_chunk_word_spacing_07(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.7,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_07.pdf")

    def test_chunk_word_spacing_08(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.8,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_08.pdf")

    def test_chunk_word_spacing_09(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Chunk(
                "Lorem Ipsum",
                border_color=X11Color.RED,
                border_width_top=1,
                border_width_right=1,
                border_width_bottom=1,
                border_width_left=1,
                word_spacing=0.9,
            )
        )

        PDF.write(what=d, where_to="assets/test_chunk_word_spacing_09.pdf")
