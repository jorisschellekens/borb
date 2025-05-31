import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.watermark import Watermark
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestWatermarkAlignment(unittest.TestCase):

    def test_watermark_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_left_top.pdf")

    def test_watermark_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_left_middle.pdf")

    def test_watermark_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_left_bottom.pdf")

    def test_watermark_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_middle_top.pdf")

    def test_watermark_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_middle_middle.pdf")

    def test_watermark_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_middle_bottom.pdf")

    def test_watermark_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_right_top.pdf")

    def test_watermark_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_right_middle.pdf")

    def test_watermark_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        Watermark(
            text="borb 2024",
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(available_space=(0, 0, 100, 100), page=p)

        PDF.write(what=d, where_to="assets/test_watermark_right_bottom.pdf")
