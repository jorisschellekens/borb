import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF

from ptext.toolkit.export.pdf_to_mp3 import PDFToMP3
from tests.test import Test
from tests.util import get_output_dir

logging.basicConfig(filename="../../logs/test_export_to_mp3.log", level=logging.DEBUG)


class TestExportToMP3(Test):
    """
    This test attempts to export each PDF in the corpus to MP3
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-export-to-mp3")

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203_page_0.pdf"))

    @unittest.skip
    def test_corpus(self):
        super(TestExportToMP3, self).test_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = PDFToMP3()
            doc = PDF.loads(pdf_file_handle, [l])
            output_file = self.output_dir / (file.stem + ".mp3")
            l.get_audio_file_per_page(0, output_file)


if __name__ == "__main__":
    unittest.main()
