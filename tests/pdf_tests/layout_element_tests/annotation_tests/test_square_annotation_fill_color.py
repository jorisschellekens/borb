import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.square_annotation import SquareAnnotation
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestSquareAnnotationFillColor(unittest.TestCase):

    def test_square_annotation_fill_color(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        SquareAnnotation(
            contents="Hello World",
            size=(100, 100),
            fill_color=X11Color.ALICE_BLUE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_square_annotation_fill_color.pdf")
