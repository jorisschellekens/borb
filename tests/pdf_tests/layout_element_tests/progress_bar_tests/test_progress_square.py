import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.progress_bar.progress_square import ProgressSquare
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestProgressSquare(unittest.TestCase):

    def test_progress_square_000(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=0,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_000.pdf")

    def test_progress_square_010(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=10,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_010.pdf")

    def test_progress_square_020(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=20,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_020.pdf")

    def test_progress_square_030(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=30,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_030.pdf")

    def test_progress_square_040(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=40,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_040.pdf")

    def test_progress_square_050(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=50,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_050.pdf")

    def test_progress_square_060(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=60,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_060.pdf")

    def test_progress_square_070(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=70,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_070.pdf")

    def test_progress_square_080(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=80,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_080.pdf")

    def test_progress_square_090(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=90,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_090.pdf")

    def test_progress_square_100(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=100,
            max_value=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_progress_square_100.pdf")
