import random

from borb.pdf import (
    SingleColumnLayout,
    PageLayout,
    Paragraph,
    Lipsum,
    LayoutElement,
    X11Color,
)
from borb.pdf.document import Document
from borb.pdf.layout_element.image.watermark import Watermark
from borb.pdf.page import Page
from tests.test_case import TestCase


class TestWatermark(TestCase):

    def test_watermark(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        random.seed(0)
        for _ in range(0, 5):
            l.append_layout_element(
                Paragraph(
                    Lipsum.generate_lorem_ipsum(512),
                    text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                )
            )

        l.append_layout_element(
            Watermark(text="CONFIDENTIAL", font_size=40, font_color=X11Color.DARK_RED)
        )

        TestCase.write(what=d, where_to="test_watermark.pdf")
