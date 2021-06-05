import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.image.simple_image_extraction import (
    SimpleImageExtraction,
)
from ptext.toolkit.ocr.ocr_image_render_event_listener import (
    OCRImageRenderEventListener,
)


class TestExtractTextUsingOCR(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_extract_images_from_pdf(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = OCRImageRenderEventListener(
                Path("/home/joris/Downloads/tessdata-master/")
            )
            doc = PDF.loads(pdf_file_handle, [l])

        return True


if __name__ == "__main__":
    unittest.main()
