import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit.export.pdf_to_mp3 import PDFToMP3
from tests.test_case import TestCase


class TestExportPDFToMP3(TestCase):
    """
    This test attempts to export each PDF in the corpus to MP3
    """

    def test_export_pdf_to_mp3(self):
        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = PDFToMP3()
            doc = PDF.loads(pdf_file_handle, [l])
            with open(
                self.get_artifacts_directory() / "output.mp3", "wb"
            ) as mp3_file_handle:
                mp3_file_handle.write(l.convert_to_mp3()[0])


if __name__ == "__main__":
    unittest.main()
