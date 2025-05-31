import unittest

from borb.pdf import (
    PDF,
    Document,
    Page,
    SingleColumnLayout,
    Paragraph,
    PageLayout,
    X11Color,
    Lipsum,
    Image,
)
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_document_as_graphml import GetDocumentAsGraphML
from borb.pdf.toolkit.source.operator.source import Source


class TestGetDocumentAsGraphML(unittest.TestCase):

    def test_get_document_as_graphml(self):

        # step 1: build PDF
        d: Document = Document()
        p: Page = Page()
        d.append_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(32),
                font_size=20,
                font_color=X11Color.PRUSSIAN_BLUE,
            )
        )
        l.append_layout_element(
            Image(
                bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1732130318657-c8740c0f5215",
                size=(128, 128),
            )
        )
        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(512)))
        PDF.write(what=d, where_to="assets/output.pdf")

        # step 2: read PDF
        d: Document = PDF.read("assets/output.pdf")

        # step 3: process
        text = Pipeline(
            [Source(), GetDocumentAsGraphML(where_to="assets/output.graphml")]
        ).process(d)
