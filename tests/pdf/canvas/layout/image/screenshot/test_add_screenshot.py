import unittest

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.image.screenshot import ScreenShot
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddScreenShot(TestCase):
    """
    This test creates a PDF with an Image in it, this Image is a ScreenShot
    """

    def test_add_screenshot(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.add_page(page)

        # add Image
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an Image in it, "
                "this Image is a ScreenShot"
            )
        )

        # add image
        layout.add(
            ScreenShot(
                width=Decimal(256),
                height=Decimal(256),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())


if __name__ == "__main__":
    unittest.main()
