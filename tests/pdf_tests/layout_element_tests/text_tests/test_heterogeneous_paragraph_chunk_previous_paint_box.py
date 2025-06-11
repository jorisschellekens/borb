import unittest

from borb.pdf import Shape, X11Color
from borb.pdf.document import Document
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestHeterogeneousParagraphChunkPreviousPaintBox(unittest.TestCase):

    def test_heterogeneous_paragraph_chunk_previous_paint_box_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        marked_chunk: Chunk = Chunk(
            "Ut enim ad minim veniam", font=Standard14Fonts.get("Helvetica-Bold")
        )
        HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                marked_chunk,
                Chunk(
                    ", quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        # paint a border around the marked chunk
        # thus proving the chunk's previous_paint_box has been set properly
        x, y, w, h = marked_chunk.get_previous_paint_box()
        Shape(
            coordinates=[(x, y), (x, y + h), (x + w, y + h), (x + w, y), (x, y)],
            fill_color=None,
            stroke_color=X11Color.RED,
        ).paint(available_space=(x, y, w, h), page=p)

        PDF.write(
            what=d,
            where_to="assets/test_heterogeneous_paragraph_chunk_previous_paint_box_001.pdf",
        )
