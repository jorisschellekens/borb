import unittest

from borb.pdf import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.equation import Equation
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestEquation(unittest.TestCase):

    def test_equation(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Equation(
            latex_syntax=r"x = \frac {-b \pm \sqrt{b^2 -4ac}} {2a}",
            font_color=X11Color.YELLOW_MUNSELL,
            font_size=12,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_equation.pdf")
