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
    filename=Path(get_log_dir(), "test-add-all-rubber-stamp-annotations.log"),
    level=logging.DEBUG,
)


class TestAddAllRubberStampAnnotations(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.input_file = Path("/home/joris/Code/pdf-corpus/0203.pdf")
        self.output_file = Path(
            get_output_dir(), "test-add-all-rubber-stamp-annotations/output.pdf"
        )

    def test_all_add_rubber_stamp_annotations(self):

        # create output directory if it does not exist yet
        if not self.output_file.parent.exists():
            self.output_file.parent.mkdir()

        # attempt to read PDF
        doc = None
        with open(self.input_file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)

        # add annotation
        for index, name in enumerate(RubberStampAnnotationIconType):
            doc.get_page(0).append_stamp_annotation(
                name=name,
                contents="Approved by Joris Schellekens",
                color=X11Color("White"),
                rectangle=Rectangle(
                    Decimal(128), Decimal(128 + index * 34), Decimal(64), Decimal(32)
                ),
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
