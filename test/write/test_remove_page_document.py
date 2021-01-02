import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from test.base_test import BaseTest

logging.basicConfig(
    filename="../write/test_remove_page_document.log", level=logging.DEBUG
)


class TestRemovePageDocument(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../write/remove_page")

    def test_single_document(self):
        self.input_file = self.input_dir / "0200.pdf"
        super().test_single_document()

    def test_against_previous_fails(self):
        super().test_against_previous_fails()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):
        if "0287" in file.stem:
            return
        if "0190" in file.stem:
            return
        if "0399" in file.stem:
            return
        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        # attempt to read PDF
        doc = None
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)

        number_of_pages = int(doc.get_document_info().get_number_of_pages())
        if number_of_pages == 1:
            return

        # remove page
        doc.pop_page(0)

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)
