import unittest
from pathlib import Path

from ptext.object.canvas.listener.color.color_spectrum_extraction import (
    ColorSpectrumExtraction,
)
from ptext.object.canvas.listener.image.simple_image_extraction import (
    SimpleImageExtraction,
)
from ptext.pdf import PDF
from ptext.test.base_test import BaseTest


class TestExtractImages(BaseTest):
    """
    This test attempts to extract the colors for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("img")

    def test_single_document(self):
        self.input_file = self.input_dir / "document_556_single_page.pdf"
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

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


if __name__ == "__main__":
    unittest.main()
