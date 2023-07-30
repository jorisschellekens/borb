import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit.image.image_extraction import ImageExtraction
from tests.test_case import TestCase


class TestExtractImages(TestCase):
    def test_extract_images_from_pdf(self):

        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = ImageExtraction()
            doc = PDF.loads(pdf_file_handle, [l])

            for i, img in enumerate(l.get_images()[0]):
                with open(
                    self.get_artifacts_directory() / ("image_%d.jpg" % i), "wb"
                ) as image_file_handle:
                    img.save(image_file_handle)

        return True


if __name__ == "__main__":
    unittest.main()
