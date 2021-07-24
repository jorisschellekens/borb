import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit.export.pdf_to_jpg import PDFToJPG


class TestExportPDFToJPG(unittest.TestCase):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

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

    def test_convert_pdf_to_jpg_001(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = PDFToJPG()
            doc = PDF.loads(pdf_file_handle, [l])
            im = l.get_image_for_page(0)
            im.save(self.output_dir / "output_001.jpg")

        return True

    def test_convert_pdf_to_jpg_002(self):
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        PDFToJPG.convert_pdf_to_jpg(input_file, 0).save(
            self.output_dir / "output_002.jpg"
        )


if __name__ == "__main__":
    unittest.main()
