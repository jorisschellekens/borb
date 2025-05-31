import random
import unittest

from borb.pdf import Paragraph, X11Color, Lipsum
from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.meta.circular_layout_element_group import (
    CircularLayoutElementGroup,
)
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestCircularLayoutElementGroupAlignment(unittest.TestCase):

    @staticmethod
    def __get_layout_element_group(
        horizontal_alignment: LayoutElement.HorizontalAlignment,
        vertical_alignment: LayoutElement.VerticalAlignment,
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
            vertical_alignment=vertical_alignment,
        )

    def test_circular_layout_element_group_alignment_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_left_top.pdf",
        )

    def test_circular_layout_element_group_alignment_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_left_middle.pdf",
        )

    def test_circular_layout_element_group_alignment_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_left_bottom.pdf",
        )

    def test_circular_layout_element_group_alignment_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_middle_top.pdf",
        )

    def test_circular_layout_element_group_alignment_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_middle_middle.pdf",
        )

    def test_circular_layout_element_group_alignment_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_middle_bottom.pdf",
        )

    def test_circular_layout_element_group_alignment_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_right_top.pdf",
        )

    def test_circular_layout_element_group_alignment_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_right_middle.pdf",
        )

    def test_circular_layout_element_group_alignment_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            TestCircularLayoutElementGroupAlignment.__get_layout_element_group(
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            ).paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(
            what=d,
            where_to=f"assets/test_circular_layout_element_group_alignment_right_bottom.pdf",
        )
