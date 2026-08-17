import random

from borb.pdf import (
    Document,
    Page,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    Image,
    X11Color,
    Lipsum,
)
from borb.pdf.toolkit.filter.font.by_font_color import ByFontColor
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_text import GetText
from borb.pdf.toolkit.source.operator.source import Source
from tests.test_case import TestCase


class TestGetText(TestCase):

    def test_get_text(self):

        # step 1: build PDF
        d: Document = Document()
        p: Page = Page()
        d.append_page(p)
        l: PageLayout = SingleColumnLayout(p)

        # add text
        random.seed(0)
        l.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(32),
                font_size=20,
                font_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # add image
        l.append_layout_element(
            Image(
                bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1732130318657-c8740c0f5215",
                size=(128, 128),
            )
        )

        # add text
        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(512)))
        TestCase.write(what=d, where_to="test_get_text.pdf")

        # step 2: read PDF
        d: Document = TestCase.read("test_get_text.pdf")

        # step 3: process
        text = Pipeline(
            [
                Source(),
                ByFontColor(font_color=X11Color.BLACK),
                GetText(),
            ]
        ).process(d)

        # step 4: check some stuff
        assert 0 in text
        assert len(text[0]) > 0
        assert len(text[0]) < 2000

    def test_get_text_from_small_document(self):

        # create PDF
        d: Document = Document()
        p: Page = Page()
        d.append_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(Paragraph("Hello world!"))
        TestCase.write(what=d, where_to="test_get_text_from_small_document.pdf")

        # read
        d = TestCase.read("test_get_text_from_small_document.pdf")

        # get text
        Pipeline([Source(), GetText()]).process(d)
