import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestFlexibleColumnWidthTableAlignment(unittest.TestCase):

    @staticmethod
    def get_table(
        h: LayoutElement.HorizontalAlignment, v: LayoutElement.VerticalAlignment
    ) -> Table:
        return (
            FlexibleColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                horizontal_alignment=h,
                vertical_alignment=v,
            )
            .append_layout_element(Chunk("Lorem"))
            .append_layout_element(Chunk("Ipsum"))
            .append_layout_element(Chunk("Dolor"))
            .append_layout_element(Chunk("Sit"))
            .append_layout_element(Chunk("Amet"))
            .append_layout_element(Chunk("Consectetur"))
            .set_padding_on_all_cells(
                padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
            )
        )

    def test_flexible_column_width_table_alignment_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_left_top.pdf",
        )

    def test_flexible_column_width_table_alignment_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_left_middle.pdf",
        )

    def test_flexible_column_width_table_alignment_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.LEFT,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_left_bottom.pdf",
        )

    def test_flexible_column_width_table_alignment_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_middle_top.pdf",
        )

    def test_flexible_column_width_table_alignment_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_middle_middle.pdf",
        )

    def test_flexible_column_width_table_alignment_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.MIDDLE,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_middle_bottom.pdf",
        )

    def test_flexible_column_width_table_alignment_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_right_top.pdf",
        )

    def test_flexible_column_width_table_alignment_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_right_middle.pdf",
        )

    def test_flexible_column_width_table_alignment_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        TestFlexibleColumnWidthTableAlignment.get_table(
            h=LayoutElement.HorizontalAlignment.RIGHT,
            v=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_flexible_column_width_table_alignment_right_bottom.pdf",
        )
