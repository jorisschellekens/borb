import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit.export.pdf_to_mp3 import PDFToMP3


class TestExportToMP3(unittest.TestCase):
    """
    This test attempts to export each PDF in the corpus to MP3
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

    def test_export_pdf_to_mp3(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = PDFToMP3()
            doc = PDF.loads(pdf_file_handle, [l])
            l.get_audio_for_page(0, self.output_dir / "output.mp3")


if __name__ == "__main__":
    unittest.main()
