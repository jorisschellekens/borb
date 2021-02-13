import logging
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.pdf import PDF
from ptext.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test import Test

logging.basicConfig(
    filename="../annotations/test-add-square-annotation-around-regular-expression.log",
    level=logging.DEBUG,
)


class TestAddSquareAnnotationAroundRegularExpression(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            "../annotations/test-add-square-annotation-around-regular-expression"
        )

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0300.pdf"))

    def test_corpus(self):
        super(TestAddSquareAnnotationAroundRegularExpression, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        # attempt to read PDF
        doc = None
        l = RegularExpressionTextExtraction("[fF]ire")
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle, [l])

        # add annotation
        print(
            "\tAdding %d annotations"
            % len(l.get_matched_text_render_info_events_per_page(0))
        )
        for e in l.get_matched_text_render_info_events_per_page(0):
            baseline = e.get_baseline()
            doc.get_page(0).append_square_annotation(
                rectangle=Rectangle(
                    Decimal(baseline.x0),
                    Decimal(baseline.y0 - 2),
                    Decimal(baseline.x1 - baseline.x0),
                    Decimal(12),
                ),
                stroke_color=X11Color("Firebrick"),
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
