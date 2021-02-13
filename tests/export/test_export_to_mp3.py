import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from ptext.toolkit.export.audio_export import AudioExport
from ptext.toolkit.structure.simple_structure_extraction import (
    SimpleStructureExtraction,
)
from tests.test import Test

logging.basicConfig(filename="../export/test_export_to_mp3.log", level=logging.DEBUG)


class TestExportToMP3(Test):
    """
    This test attempts to export each PDF in the corpus to MP3
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../export/test-export-to-mp3")

    def test_corpus(self):
        super(TestExportToMP3, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = AudioExport()
            doc = PDF.loads(pdf_file_handle, [SimpleStructureExtraction(), l])
            output_file = self.output_dir / (file.stem + ".mp3")
            l.get_audio_file_per_page(0, output_file)


if __name__ == "__main__":
    unittest.main()
