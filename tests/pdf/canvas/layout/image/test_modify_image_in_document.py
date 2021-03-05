import logging
import unittest
from pathlib import Path

from PIL import Image as PILImage

from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-modify-image-in-document.log", level=logging.DEBUG
)


class TestModifyImageInDocument(unittest.TestCase):
    """
    This test attempts to read the DocumentInfo for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-modify-image-in-document")

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

    def test_write_document(self) -> bool:

        # read input
        doc = None
        with open("/home/joris/Code/pdf-corpus/0203.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # read images
        xobjects = doc["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][0]["Resources"][
            "XObject"
        ]

        # modify image(s)
        for k, v in xobjects.items():
            if isinstance(v, PILImage.Image):
                self._modify_image(v)

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        return True


if __name__ == "__main__":
    unittest.main()
