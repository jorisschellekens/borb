import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.form.text_box import TextBox
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestTextBoxBackground(unittest.TestCase):

    def test_text_box_background(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TextBox(
            padding_top=5,
            padding_bottom=5,
            padding_right=5,
            padding_left=5,
            background_color=X11Color.YELLOW_MUNSELL,
        ).paint(available_space=(x, y, w, h), page=p)

        PDF.write(what=d, where_to="assets/test_text_box_background.pdf")
