import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.free_text_annotation import FreeTextAnnotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestFreeTextAnnotation(unittest.TestCase):

    def test_free_text_annotation_text_alignment_left(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        FreeTextAnnotation(
            contents=Lipsum.generate_lorem_ipsum(50),
            text_alignment=LayoutElement.TextAlignment.LEFT,
            size=(100, 100),
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_free_text_annotation_text_alignment_left.pdf"
        )

    def test_free_text_annotation_text_alignment_centered(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        FreeTextAnnotation(
            contents=Lipsum.generate_lorem_ipsum(50),
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            size=(100, 100),
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_free_text_annotation_text_alignment_centered.pdf",
        )

    def test_free_text_annotation_text_alignment_right(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        FreeTextAnnotation(
            contents=Lipsum.generate_lorem_ipsum(50),
            text_alignment=LayoutElement.TextAlignment.RIGHT,
            size=(100, 100),
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(
            what=d, where_to="assets/test_free_text_annotation_text_alignment_right.pdf"
        )
