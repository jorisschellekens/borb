import typing
import unittest
from decimal import Decimal

from borb.io.read.types import Decimal
from borb.pdf import Document
from borb.pdf import Image
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddImageFromURL(TestCase):
    """
    This test creates a PDF with a (PNG) Image in it, this is specified by a URL
    """

    def _get_image_001(self) -> typing.Any:
        return Image(
            "https://d262ijfj3ea8g5.cloudfront.net/2017/img/logo.png",
            width=Decimal(64),
            height=Decimal(64),
        )

    def _get_image_002(self) -> typing.Any:
        return Image(
            "https://www.mozilla.org/media/protocol/img/logos/firefox/browser/logo-lg-high-res.fbc7ffbb50fd.png",
            width=Decimal(64),
            height=Decimal(64),
        )

    def _get_image_003(self) -> typing.Any:
        img: Image = Image(
            "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48",
        )
        img.force_load_image()
        return Image(img._image.convert("L"), width=Decimal(64), height=Decimal(64))

    def test_add_compressed_image_from_url(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an Image in it, this is specified by a URL. "
                "The server uses compression. This would previously fail with an UnidentifiedImageError"
            )
        )
        layout.add(self._get_image_001())
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_png_image_from_url(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an Image in it, this is specified by a URL. "
                "The Image is a PNG image."
            )
        )
        layout.add(self._get_image_002())
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_grayscale_image_from_url(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an Image in it, this is specified by a URL. "
                "The Image is a grayscale image."
            )
        )
        layout.add(self._get_image_003())
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())


if __name__ == "__main__":
    unittest.main()
