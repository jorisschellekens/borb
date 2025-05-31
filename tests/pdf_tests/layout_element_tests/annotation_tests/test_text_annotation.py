import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.text_annotation import TextAnnotation
from borb.pdf.lipsum.lipsum import Lipsum
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestTextAnnotation(unittest.TestCase):

    def test_text_annotation(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # add StrikeOutAnnotation
        TextAnnotation(
            contents=Lipsum.generate_lorem_ipsum(100),
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

        PDF.write(what=d, where_to="assets/test_text_annotation.pdf")
