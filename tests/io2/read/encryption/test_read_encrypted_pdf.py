from pathlib import Path

from borb.pdf import PDF
from borb.toolkit import SimpleTextExtraction
from tests.test_case import TestCase


class TestReadEncryptedPDF(TestCase):
    def test_open_encrypted_pdf(self):
        input_file: Path = self.get_artifacts_directory(True) / "input_001.pdf"
        with open(input_file, "rb") as fh:
            PDF.loads(fh, password="appeltje")

    def test_read_encrypted_pdf(self):
        input_file: Path = self.get_artifacts_directory(True) / "input_001.pdf"

        # open
        l: SimpleTextExtraction = SimpleTextExtraction()
        with open(input_file, "rb") as fh:
            PDF.loads(fh, password="appeltje", event_listeners=[l])

        # compare text
        text: str = l.get_text()[0]
        assert text.startswith(
            "Video provides a powerful way to help you prove your point."
        )
