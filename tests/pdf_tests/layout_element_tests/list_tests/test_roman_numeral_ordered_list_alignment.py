import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.roman_numeral_ordered_list import (
    RomanNumeralOrderedList,
)
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestRomanNumeralOrderedListAlignment(unittest.TestCase):

    def test_roman_numeral_ordered_list_alignment_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
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

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_left_top.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_left_middle.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
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

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_left_bottom.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
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

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_middle_top.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_middle_middle.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
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

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_middle_bottom.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
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

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_right_top.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            )
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to="assets/test_roman_numeral_ordered_list_alignment_right_middle.pdf",
        )

    def test_roman_numeral_ordered_list_alignment_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            RomanNumeralOrderedList(
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

        PDF.write(
            what=d,
            where_to=f"assets/test_roman_numeral_ordered_list_alignment_right_bottom.pdf",
        )
