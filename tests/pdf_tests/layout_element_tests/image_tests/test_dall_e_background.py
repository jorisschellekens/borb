import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.dall_e import DallE
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestDallEBackground(unittest.TestCase):

    @unittest.skip
    def test_dall_e_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        try:
            from tests.secrets import populate_os_environ

            populate_os_environ()
        except:
            pass
        DallE(
            prompt="A rotund yellow bird, enjoying life",
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(80, 80),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_dall_e_background.pdf")
