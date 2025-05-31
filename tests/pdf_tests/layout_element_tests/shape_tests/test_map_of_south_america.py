import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.shape.map_of_south_america import MapOfSouthAmerica
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestMapOfSouthAmerica(unittest.TestCase):

    def test_map_of_south_america(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        MapOfSouthAmerica(
            fill_color=X11Color.LIGHT_GRAY, stroke_color=X11Color.WHITE, line_width=0.1
        ).set_fill_color(fill_color=X11Color.YELLOW_MUNSELL, name="Brazil").paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_map_of_south_america.pdf")
