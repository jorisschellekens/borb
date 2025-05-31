import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestHeterogeneousParagraphPreservesChunkProperties(unittest.TestCase):

    def test_heterogeneous_paragraph_preserves_font_color(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk("Ut enim ad minim veniam, ", font_color=X11Color.YELLOW_MUNSELL),
                Chunk(
                    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
            border_width_top=1,
            border_width_right=1,
            border_width_bottom=1,
            border_width_left=1,
            border_color=X11Color.RED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_heterogeneous_paragraph_preserves_font_color.pdf",
        )

    def test_heterogeneous_paragraph_preserves_font(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk(
                    "Ut enim ad minim veniam, ",
                    font=Standard14Fonts.get("Helvetica-Bold"),
                ),
                Chunk(
                    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_heterogeneous_paragraph_preserves_font.pdf"
        )

    def test_heterogeneous_paragraph_preserves_font_size(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk("Ut enim ad minim veniam, ", font_size=10),
                Chunk(
                    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_heterogeneous_paragraph_preserves_font_size.pdf",
        )

    def test_heterogeneous_paragraph_preserves_border(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk(
                    "Ut enim ad minim veniam, ",
                    border_width_left=1,
                    border_width_top=1,
                    border_width_right=1,
                    border_width_bottom=1,
                    border_color=X11Color.YELLOW_MUNSELL,
                ),
                Chunk(
                    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_heterogeneous_paragraph_preserves_border.pdf"
        )

    def test_heterogeneous_paragraph_preserves_background_color(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk(
                    "Ut enim ad minim veniam, ",
                    background_color=X11Color.YELLOW_MUNSELL,
                ),
                Chunk(
                    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_heterogeneous_paragraph_preserves_background.pdf",
        )
