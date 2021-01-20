import logging
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../annotations/test-add-redact-annotation.log", level=logging.DEBUG
)


class TestAddRedactAnnotation(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../annotations/test-add-redact-annotation")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0200.pdf"))

    def test_corpus(self):
        super(TestAddRedactAnnotation, self).test_corpus()

    def test_document(self, file):

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

        # add annotation
        doc.get_page(0).append_redact_annotation(
            overlay_text="Lorem Ipsum",
            repeat_overlay_text=True,
            interior_color=X11Color("AliceBlue"),
            rectangle=(Decimal(256), Decimal(256), Decimal(128), Decimal(128)),
        )

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)

        return True
