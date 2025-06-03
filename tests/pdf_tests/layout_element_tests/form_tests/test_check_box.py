import unittest

from borb.pdf import CheckBox
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCheckBox(unittest.TestCase):

    def test_check_box(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        CheckBox().paint(available_space=(x, y, w, h), page=p)

        PDF.write(what=d, where_to="assets/test_check_box.pdf")
