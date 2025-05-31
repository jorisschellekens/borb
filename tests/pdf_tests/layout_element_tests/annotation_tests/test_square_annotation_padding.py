import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.square_annotation import SquareAnnotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestSquareAnnotationPadding(unittest.TestCase):

    def test_square_annotation_padding_left(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        SquareAnnotation(
            size=(100, 100),
            padding_left=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_square_annotation_padding_left.pdf")

    def test_square_annotation_padding_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        SquareAnnotation(
            size=(100, 100),
            padding_top=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_square_annotation_padding_top.pdf")

    def test_square_annotation_padding_right(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        SquareAnnotation(
            size=(100, 100),
            padding_right=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_square_annotation_padding_right.pdf")

    def test_square_annotation_padding_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        SquareAnnotation(
            size=(100, 100),
            padding_bottom=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_square_annotation_padding_bottom.pdf")
