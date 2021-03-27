import logging
import unittest
from pathlib import Path

from ptext.pdf.document import Document
from ptext.pdf.pdf import PDF
from tests.test import Test
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-concat-documents.log"), level=logging.DEBUG
)


class TestConcatDocuments(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-concat-documents")
        self.input_file_b = self.input_dir / "0200.pdf"

    @unittest.skip
    def test_corpus(self):
        super(TestConcatDocuments, self).test_corpus()

    def _test_document(self, file):

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
        for i in range(0, int(doc_a.get_document_info().get_number_of_pages())):
            doc_c.append_page(doc_a.get_page(i))
        for i in range(0, int(doc_b.get_document_info().get_number_of_pages())):
            doc_c.append_page(doc_b.get_page(i))

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twrite ..")
            PDF.dumps(out_file_handle, doc_c)

        return True
