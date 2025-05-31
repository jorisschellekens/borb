import random
import unittest

from borb.pdf.color.hex_color import HexColor
from borb.pdf.document import Document
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestFlexibleColumnWidthTable(unittest.TestCase):

    def test_flexible_column_width_table_of_shape(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        random.seed(0)
        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .append_layout_element(
                LineArt.blob(
                    fill_color=HexColor("a5ffd6"),
                    stroke_color=HexColor("a5ffd6").darker(),
                )
            )
            .append_layout_element(
                LineArt.blob(
                    fill_color=HexColor("56cbf9"),
                    stroke_color=HexColor("56cbf9").darker(),
                )
            )
            .append_layout_element(
                LineArt.blob(
                    fill_color=HexColor("0b3954"),
                    stroke_color=HexColor("0b3954").darker(),
                )
            )
            .append_layout_element(
                LineArt.blob(
                    fill_color=HexColor("f1cd2e"),
                    stroke_color=HexColor("f1cd2e").darker(),
                )
            )
            .append_layout_element(
                LineArt.blob(
                    fill_color=HexColor("de6449"),
                    stroke_color=HexColor("de6449").darker(),
                )
            )
            .append_layout_element(
                LineArt.blob(
                    fill_color=HexColor("ffffff"),
                    stroke_color=HexColor("000000").darker(),
                )
            )
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_flexible_column_width_table_of_shape.pdf"
        )

    def test_flexible_column_width_table_of_chunk(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .append_layout_element(Chunk("Lorem"))
            .append_layout_element(Chunk("Ipsum"))
            .append_layout_element(Chunk("Dolor"))
            .append_layout_element(Chunk("Sit"))
            .append_layout_element(Chunk("Amet"))
            .append_layout_element(Chunk("Consectetur"))
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_flexible_column_width_table_of_chunk.pdf"
        )

    def test_flexible_column_width_table_of_paragraph(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .append_layout_element(
                Paragraph(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                )
            )
            .append_layout_element(
                Paragraph(
                    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                )
            )
            .append_layout_element(
                Paragraph(
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
                )
            )
            .append_layout_element(
                Paragraph(
                    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                )
            )
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_flexible_column_width_table_of_paragraph.pdf"
        )

    def test_flexible_column_width_table_of_images(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .append_layout_element(
                Image(
                    "https://images.unsplash.com/photo-1484189896464-00489dba2a45",
                    size=(80, 80),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )
            .append_layout_element(
                Image(
                    "https://images.unsplash.com/photo-1515876879333-013aa5ea1472",
                    size=(80, 80),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )
            .append_layout_element(
                Image(
                    "https://images.unsplash.com/photo-1492831379069-0fe9d118b7c5",
                    size=(80, 80),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )
            .append_layout_element(
                Image(
                    "https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
                    size=(80, 80),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )
            .append_layout_element(
                Image(
                    "https://images.unsplash.com/photo-1458791087439-278afc90b1d5",
                    size=(80, 80),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )
            .append_layout_element(
                Image(
                    "https://images.unsplash.com/photo-1457286758722-055a4c6e6666",
                    size=(80, 80),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_flexible_column_width_table_of_images.pdf"
        )

    def test_flexible_column_width_table_of_lists(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .append_layout_element(
                UnorderedList()
                .append_layout_element(Chunk("Ipsum"))
                .append_layout_element(Chunk("Dolor"))
            )
            .append_layout_element(
                UnorderedList()
                .append_layout_element(Chunk("Ipsum"))
                .append_layout_element(Chunk("Dolor"))
                .append_layout_element(Chunk("Sit"))
            )
            .append_layout_element(
                UnorderedList()
                .append_layout_element(Chunk("Sit"))
                .append_layout_element(Chunk("Amet"))
                .append_layout_element(Chunk("Consectetur"))
            )
            .append_layout_element(
                UnorderedList()
                .append_layout_element(Chunk("Ipsum"))
                .append_layout_element(Chunk("Consectetur"))
            )
            .append_layout_element(
                UnorderedList()
                .append_layout_element(Chunk("Sit"))
                .append_layout_element(Chunk("Amet"))
            )
            .append_layout_element(
                UnorderedList()
                .append_layout_element(Chunk("Ipsum"))
                .append_layout_element(Chunk("Dolor"))
                .append_layout_element(Chunk("Sit"))
                .append_layout_element(Chunk("Amet"))
                .append_layout_element(Chunk("Consectetur"))
            )
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_flexible_column_width_table_of_list.pdf"
        )
