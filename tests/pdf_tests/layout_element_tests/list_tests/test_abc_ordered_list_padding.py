import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.abc_ordered_list import ABCOrderedList
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestABCOrderedOrderedListPadding(unittest.TestCase):

    def test_abc_ordered_list_padding_left(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            ABCOrderedList(
                padding_left=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to=f"assets/test_abc_ordered_list_padding_left.pdf")

    def test_abc_ordered_list_padding_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            ABCOrderedList(
                padding_top=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to=f"assets/test_abc_ordered_list_padding_top.pdf")

    def test_abc_ordered_list_padding_right(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            ABCOrderedList(
                padding_right=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to=f"assets/test_abc_ordered_list_padding_right.pdf")

    def test_abc_ordered_list_padding_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            ABCOrderedList(
                padding_bottom=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to=f"assets/test_abc_ordered_list_padding_bottom.pdf")
