import logging
import unittest
from pathlib import Path

import requests
from PIL import Image as PILImage

from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-image.log", level=logging.DEBUG
)


class TestWriteImage(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-write-image")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add Image
        layout = SingleColumnLayout(page)

        im = PILImage.open(
            requests.get(
                "https://365psd.com/images/listing/fbe/ups-logo-49752.jpg", stream=True
            ).raw
        )
        layout.add(Image(im))

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
