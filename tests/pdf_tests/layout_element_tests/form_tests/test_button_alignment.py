import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.form.button import Button
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestButtonAlignment(unittest.TestCase):

    def test_button_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_left_top.pdf")

    def test_button_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_left_middle.pdf")

    def test_button_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_left_bottom.pdf")

    def test_button_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_middle_top.pdf")

    def test_button_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_middle_middle.pdf")

    def test_button_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_middle_bottom.pdf")

    def test_button_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_right_top.pdf")

    def test_button_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_right_middle.pdf")

    def test_button_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Button(
            text="Lorem",
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_button_right_bottom.pdf")
