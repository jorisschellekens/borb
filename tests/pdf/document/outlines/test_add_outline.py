import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../../../logs/test-add-outline.log", level=logging.DEBUG)


class TestAddOutline(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../output/test-add-outline")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_corpus(self):
        super(TestAddOutline, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + ".pdf")

        # attempt to read PDF
        doc = None
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)

        doc.add_outline("Lorem", 0, page_nr=0, destination_type="Fit")
        doc.add_outline("Ipsum", 0, page_nr=1, destination_type="Fit")
        doc.add_outline("Dolor", 1, page_nr=0, destination_type="Fit")
        doc.add_outline("Sit", 2, page_nr=1, destination_type="Fit")
        doc.add_outline("Amet", 3, page_nr=0, destination_type="Fit")
        doc.add_outline("Consectetur", 3, page_nr=1, destination_type="Fit")
        doc.add_outline("Adipiscing", 3, page_nr=0, destination_type="Fit")
        doc.add_outline("Elit", 1, page_nr=1, destination_type="Fit")

        with open(out_file, "wb") as out_file_handle:
            print("\twrite ..")
            PDF.dumps(out_file_handle, doc)

        return True
