import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.watermark import Watermark
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestWatermark(unittest.TestCase):

    def test_watermark(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(text="borb 2024").paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark.pdf")
