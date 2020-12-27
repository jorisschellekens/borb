import logging
import unittest
from pathlib import Path

from ptext.action.export.audio_export import AudioExport
from ptext.action.structure.simple_structure_extraction import (
    SimpleStructureExtraction,
)
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(filename="test_export_to_mp3.log", level=logging.DEBUG)


class TestExportToMP3(BaseTest):
    """
    This test attempts to export each PDF in the corpus to MP3
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("audio")

    def test_single_document(self):
        super().test_single_document()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):

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
