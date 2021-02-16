import logging
from pathlib import Path

from ptext.pdf.document import Document
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../logs/test-concat-documents-2.log", level=logging.DEBUG
)


class TestConcatDocuments2(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../output/test-concat-documents-2")
        self.input_file_b = self.input_dir / "0200.pdf"

    def test_corpus(self):
        super(TestConcatDocuments2, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0200.pdf"))

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        # attempt to read PDF
        doc_a = None
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc_a = PDF.loads(in_file_handle)

        # attempt to read PDF
        with open(self.input_file_b, "rb") as in_file_handle_b:
            print("\treading (2) ..")
            doc_b = PDF.loads(in_file_handle_b)

        # concat all pages to same document
        doc_c = Document()
        doc_c.append_document(doc_a)
        doc_c.append_document(doc_b)

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twrite ..")
            PDF.dumps(out_file_handle, doc_c)

        return True
