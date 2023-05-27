import typing
import unittest
from decimal import Decimal

import requests
from PIL import Image as PILImage

from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestModifyImage(TestCase):
    """
    This test creates a PDF with an Image in it, this is specified by a URL
    and then modifies that Image
    """

    def _modify_image(self, image: PILImage.Image):
        w = image.width
        h = image.height
        pixels = image.load()
        for i in range(0, w):
            for j in range(0, h):
                r, g, b = pixels[i, j]

                # convert to sepia
                new_r = r * 0.393 + g * 0.769 + b * 0.189
                new_g = r * 0.349 + g * 0.686 + b * 0.168
                new_b = r * 0.272 + g * 0.534 + b * 0.131

                # set
                pixels[i, j] = (int(new_r), int(new_g), int(new_b))

    def test_add_image_to_pdf_001(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                "This test adds an Image to PDF and a subsequent test modifies that Image."
            )
        )
        layout.add(
            Image(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                width=Decimal(256),
                height=Decimal(256),
            )
        )
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_image_to_pdf_002(self):
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None
        xobjects = doc["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][0]["Resources"][
            "XObject"
        ]
        for k, v in xobjects.items():
            if isinstance(v, PILImage.Image):
                self._modify_image(v)
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_image_to_pdf_003(self):
        doc: typing.Optional[Document] = None
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None
        replacement_image = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1667390894220-5ed48a975e85",
                stream=True,
            ).raw
        )
        image1 = doc.get_page(0)["Resources"]["XObject"]["Im1"]
        image1.paste(replacement_image)
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())


if __name__ == "__main__":
    unittest.main()
