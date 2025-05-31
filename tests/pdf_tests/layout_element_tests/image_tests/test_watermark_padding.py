import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.watermark import Watermark
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestWatermarkPadding(unittest.TestCase):

    def test_watermark_padding_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(text="borb 2024", padding_top=100).paint(
            available_space=(0, 0, 100, 100), page=p
        )

        PDF.write(what=d, where_to="assets/test_watermark_padding_top.pdf")

    def test_watermark_padding_right(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(text="borb 2024", padding_right=100).paint(
            available_space=(0, 0, 100, 100), page=p
        )

        PDF.write(what=d, where_to="assets/test_watermark_padding_right.pdf")

    def test_watermark_padding_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(text="borb 2024", padding_bottom=100).paint(
            available_space=(0, 0, 100, 100), page=p
        )

        PDF.write(what=d, where_to="assets/test_watermark_padding_bottom.pdf")

    def test_watermark_padding_left(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(text="borb 2024", padding_left=100).paint(
            available_space=(0, 0, 100, 100), page=p
        )

        PDF.write(what=d, where_to="assets/test_watermark_padding_left.pdf")
