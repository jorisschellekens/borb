import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.strike_out_annotation import StrikeOutAnnotation
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestStrikeOutAnnotationStrokeColor(unittest.TestCase):

    def test_strike_out_annotation_stroke_color(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # add StrikeOutAnnotation
        StrikeOutAnnotation(
            size=(100, 100),
            stroke_color=X11Color.PRUSSIAN_BLUE,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_strike_out_annotation_stroke_color.pdf")
