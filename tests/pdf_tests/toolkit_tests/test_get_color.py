import unittest

from borb.pdf import (
    PDF,
    Document,
    Page,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    Image,
    X11Color,
    Lipsum,
    GetColors,
)
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.source.operator.source import Source


class TestGetColor(unittest.TestCase):

    def test_get_color(self):

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
        colors = Pipeline(
            [
                Source(),
                GetColors(),
            ]
        ).process(d)

        # step 4: check some stuff
        assert 0 in colors
        assert isinstance(colors[0], dict)
        assert len(colors[0]) > 0
        print(colors[0])
