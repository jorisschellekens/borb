import unittest

from borb.pdf.document import Document
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestHeterogeneousParagraphAlignment(unittest.TestCase):

    @staticmethod
    def get_paragraph(
        h: LayoutElement.HorizontalAlignment, v: LayoutElement.VerticalAlignment
    ) -> HeterogeneousParagraph:
        return HeterogeneousParagraph(
            chunks=[
                Chunk(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                ),
                Chunk("Ut enim", font=Standard14Fonts.get("Helvetica-Bold")),
                Chunk(
                    "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                ),
            ],
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
            horizontal_alignment=h,
            vertical_alignment=v,
        )

    def test_heterogeneous_paragraph_alignment_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_left_top.pdf",
        )

    def test_heterogeneous_paragraph_alignment_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_left_middle.pdf",
        )

    def test_heterogeneous_paragraph_alignment_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_left_bottom.pdf",
        )

    def test_heterogeneous_paragraph_alignment_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_middle_top.pdf",
        )

    def test_heterogeneous_paragraph_alignment_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_middle_middle.pdf",
        )

    def test_heterogeneous_paragraph_alignment_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_middle_bottom.pdf",
        )

    def test_heterogeneous_paragraph_alignment_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_right_top.pdf",
        )

    def test_heterogeneous_paragraph_alignment_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_right_middle.pdf",
        )

    def test_heterogeneous_paragraph_alignment_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestHeterogeneousParagraphAlignment.get_paragraph(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_heterogeneous_paragraph_alignment_right_bottom.pdf",
        )
