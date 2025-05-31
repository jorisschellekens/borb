import random
import unittest

from borb.pdf import Paragraph, Lipsum, X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.meta.circular_layout_element_group import (
    CircularLayoutElementGroup,
)
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCircularLayoutElementGroupPadding(unittest.TestCase):

    @staticmethod
    def __get_layout_element_group(
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ) -> CircularLayoutElementGroup:
        random.seed(0)
        return CircularLayoutElementGroup(
            layout_elements=[
                Paragraph(
                    Lipsum.generate_lorem_ipsum(64),
                    font_size=8,
                    background_color=X11Color.YELLOW_MUNSELL,
                    text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                )
                for _ in range(0, 6)
            ],
            horizontal_alignment=horizontal_alignment,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

    def test_circular_layout_element_group_padding_left(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupPadding.__get_layout_element_group(
                padding_left=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_padding_left.pdf",
        )

    def test_circular_layout_element_group_padding_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupPadding.__get_layout_element_group(
                padding_top=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_padding_top.pdf",
        )

    def test_circular_layout_element_group_padding_right(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupPadding.__get_layout_element_group(
                padding_right=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_padding_right.pdf",
        )

    def test_circular_layout_element_group_padding_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupPadding.__get_layout_element_group(
                padding_bottom=100,
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_padding_bottom.pdf",
        )
