import unittest

import requests
from PIL import Image as PILImage

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddPILImage(TestCase):
    """
    This test creates a PDF with an Image in it, this is specified by a PIL Image
    """

    def _get_image_001(self):
        im = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                stream=True,
            ).raw
        )
        return Image(im, width=Decimal(64), height=Decimal(64))

    def test_add_PIL_image(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an Image in it, this is specified by a PIL image."
            )
        )
        layout.add(self._get_image_001())
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())


if __name__ == "__main__":
    unittest.main()
