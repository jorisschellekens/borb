import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.image.simple_image_extraction import (
    SimpleImageExtraction,
)
from tests.test import Test
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-extract-images.log"), level=logging.DEBUG
)


class TestExtractImages(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-extract-images")

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    @unittest.skip
    def test_corpus(self):
        super(TestExtractImages, self).test_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = SimpleImageExtraction()
            doc = PDF.loads(pdf_file_handle, [l])

            for i, img in enumerate(l.get_images_per_page(0)):
                output_file = self.output_dir / (file.stem + str(i) + ".jpg")
                with open(output_file, "wb") as image_file_handle:
                    img.save(image_file_handle)

        return True


if __name__ == "__main__":
    unittest.main()
