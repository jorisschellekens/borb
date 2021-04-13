import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-append-embedded-file.log"), level=logging.DEBUG
)


class TestAppendEmbeddedFile(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.input_file = Path("/home/joris/Code/pdf-corpus/0203.pdf")
        self.output_file = Path(
            get_output_dir(), "test-append-embedded-file/output.pdf"
        )

    def test_document(self):

        # create output directory if it does not exist yet
        if not self.output_file.parent.exists():
            self.output_file.parent.mkdir()

        # read document
        doc = None
        with open(self.input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # append document
        doc.append_embedded_file(
            "the_raven.txt",
            b"Once upon a midnight dreary, while I pondered weak and weary over many a quaint and curious volume of forgotten lore.",
        )

        # attempt to store PDF
        with open(self.output_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(self.output_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)

        embedded_files = doc.get_embedded_files()
        assert len(embedded_files) == 1
        assert "the_raven.txt" in embedded_files
        assert b"Once upon a midnight" in embedded_files["the_raven.txt"]
