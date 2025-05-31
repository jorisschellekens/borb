import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.rubber_stamp_annotation import (
    RubberStampAnnotation,
)
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestRubberStampAnnotationAlignment(unittest.TestCase):

    def test_rubber_stamp_annotation_left_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_left_top.pdf")

    def test_rubber_stamp_annotation_left_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_left_middle.pdf"
        )

    def test_rubber_stamp_annotation_left_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_left_bottom.pdf"
        )

    def test_rubber_stamp_annotation_middle_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_middle_top.pdf")

    def test_rubber_stamp_annotation_middle_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_middle_middle.pdf"
        )

    def test_rubber_stamp_annotation_middle_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_middle_bottom.pdf"
        )

    def test_rubber_stamp_annotation_right_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_rubber_stamp_annotation_right_top.pdf")

    def test_rubber_stamp_annotation_right_middle(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_right_middle.pdf"
        )

    def test_rubber_stamp_annotation_right_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        RubberStampAnnotation(
            size=(100, 100),
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                p.get_size()[0] // 2 - 50,
                p.get_size()[1] // 2 - 50,
                100,
                100,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_rubber_stamp_annotation_right_bottom.pdf"
        )
