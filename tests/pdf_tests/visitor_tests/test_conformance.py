import random
import unittest

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    PDF,
    PageLayout,
    GoogleTrueTypeFont,
    X11Color,
    Image,
)
from borb.pdf.conformance import Conformance
from tests.secrets import populate_os_environ


class TestConformance(unittest.TestCase):

    @staticmethod
    def __build_pdf_document(conformance: Conformance, output_path: str):
        d: Document = Document(
            conformance=conformance, on_non_conformance_print_warning=True
        )

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        # google font api
        populate_os_environ()

        # title
        random.seed(0)
        l.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(64),
                font_size=20,
                font_color=X11Color.YELLOW_MUNSELL,
                font=GoogleTrueTypeFont.from_google_font_api(name="Acme"),
            )
        )

        # body
        l.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(300),
                font_size=12,
                font=GoogleTrueTypeFont.from_google_font_api(name="Acme"),
            )
        )

        # image
        l.append_layout_element(
            Image(
                bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
                size=(200, 200),
            )
        )

        # output
        PDF.write(what=d, where_to=output_path)

    def test_pdf_a_1_a(self):
        TestConformance.__build_pdf_document(
            conformance=Conformance.PDF_A_1A, output_path="assets/test_pdf_a_1_a.pdf"
        )

    def test_pdf_a_1_b(self):
        TestConformance.__build_pdf_document(
            conformance=Conformance.PDF_A_1B, output_path="assets/test_pdf_a_1_b.pdf"
        )
