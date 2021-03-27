import logging
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.pdf import PDF
from tests.test import Test
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-add-watermark-annotation.log"),
    level=logging.DEBUG,
)


class TestAddWatermarkAnnotation(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-add-watermark-annotation")

    @unittest.skip
    def test_corpus(self):
        super(TestAddWatermarkAnnotation, self).test_corpus()

    def _test_document(self, file):

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
        doc.get_page(0).append_watermark_annotation(
            contents="pText",
            rectangle=Rectangle(Decimal(128), Decimal(128), Decimal(64), Decimal(64)),
        )

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)
