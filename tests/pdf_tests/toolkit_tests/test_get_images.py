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
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_images import GetImages
from borb.pdf.toolkit.source.operator.source import Source
from tests.test_case import TestCase


class TestGetImages(TestCase):

    def test_get_images(self):

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
        TestCase.write(what=d, where_to="test_get_images.pdf")

        # step 2: read PDF
        d: Document = TestCase.read("test_get_images.pdf")

        # step 3: process
        images = Pipeline(
            [
                Source(),
                GetImages(),
            ]
        ).process(d)

        # step 4: check some stuff
        assert 0 in images
        assert isinstance(images[0], list)
        assert len(images[0]) > 0
