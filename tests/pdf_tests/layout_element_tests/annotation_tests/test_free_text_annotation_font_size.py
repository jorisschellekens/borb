import random

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.free_text_annotation import FreeTextAnnotation
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from tests.test_case import TestCase


class TestFreeTextAnnotationFontSize(TestCase):

    def test_free_text_annotation_font_size(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        random.seed(0)
        FreeTextAnnotation(
            contents=Lipsum.generate_lorem_ipsum(50),
            font_size=20,
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

        TestCase.write(what=d, where_to="test_free_text_annotation_font_size.pdf")
