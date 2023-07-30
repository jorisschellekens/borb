import unittest

from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddXLImage(TestCase):
    """
    This test creates a PDF with an Image in it, this is specified by a URL.
    The Image is too large, and an assert is triggered.
    """

    def test_write_document_with_xl_image(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with an Image in it, this is specified by a URL. "
                "The Image is too large to fit the page."
            )
        )
        with self.assertRaises(AssertionError):
            layout.add(
                Image(
                    "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw"
                )
            )
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())


if __name__ == "__main__":
    unittest.main()
