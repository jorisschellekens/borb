import logging
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.pdf import PDF
from tests.util import get_output_dir, get_log_dir

logging.basicConfig(
    filename=Path(
        get_log_dir(), "test-add-polyline-annotation-using-line-art-factory.log"
    ),
    level=logging.DEBUG,
)


class TestAddPolylineAnnotationUsingLineArtFactory(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.input_file = Path("/home/joris/Code/pdf-corpus/0203.pdf")
        self.output_file = Path(
            get_output_dir(),
            "test-add-polyline-annotation-using-line-art-factory/output.pdf",
        )

    def test_add_polyline_annotation_using_lineart_factory(self):

        # create output directory if it does not exist yet
        if not self.output_file.parent.exists():
            self.output_file.parent.mkdir()

        # attempt to read PDF
        doc = None
        with open(self.input_file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)

        # add annotation
        doc.get_page(0).append_polyline_annotation(
            points=LineArtFactory.droplet(
                Rectangle(Decimal(100), Decimal(100), Decimal(100), Decimal(100))
            ),
            stroke_color=X11Color("Crimson"),
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
