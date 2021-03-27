import logging
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import RubberStampAnnotationIconType
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-add-rubber-stamp-annotation.log"),
    level=logging.DEBUG,
)


class TestAddRubberStampAnnotation(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.input_file = Path("/home/joris/Code/pdf-corpus/0203.pdf")
        self.output_file = Path(
            get_output_dir(), "test-add-rubber-stamp-annotation/output.pdf"
        )

    def test_add_rubber_stamp_annotation(self):

        # create output directory if it does not exist yet
        if not self.output_file.parent.exists():
            self.output_file.parent.mkdir()

        # attempt to read PDF
        doc = None
        with open(self.input_file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)

        # add annotation
        doc.get_page(0).append_stamp_annotation(
            name=RubberStampAnnotationIconType.CONFIDENTIAL,
            contents="Approved by Joris Schellekens",
            color=X11Color("Red"),
            rectangle=Rectangle(Decimal(128), Decimal(56), Decimal(132), Decimal(58)),
        )

        # attempt to store PDF
        with open(self.output_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(self.output_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)

        return True
