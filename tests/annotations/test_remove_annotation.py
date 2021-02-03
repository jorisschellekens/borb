import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../annotations/test-remove-annotation.log", level=logging.DEBUG
)


class TestRemoveAnnotation(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../annotations/remove-annotation")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0200.pdf"))

    def test_corpus(self):
        super(TestRemoveAnnotation, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        doc = None
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # remove first annotation
        if "Annots" in doc.get_page(0):
            annots = doc.get_page(0)["Annots"]
            annots[0]["P"] = None
            doc.get_page(0)["Annots"] = annots[1:0]
            pass

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)
        return True
