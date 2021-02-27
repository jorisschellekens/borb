import logging
import math
from decimal import Decimal
from pathlib import Path
from typing import Tuple, List

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../../logs/test-add-polyline-annotation-using-line-art-factory.log",
    level=logging.DEBUG,
)


class TestAddPolylineAnnotationUsingLineArtFactory(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            "../../../output/test-add-polyline-annotation-using-line-art-factory"
        )

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_corpus(self):
        super(TestAddPolylineAnnotationUsingLineArtFactory, self).test_corpus()

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
        doc.get_page(0).append_polyline_annotation(
            points=LineArtFactory.droplet(
                Rectangle(Decimal(100), Decimal(100), Decimal(100), Decimal(100))
            ),
            stroke_color=X11Color("Crimson"),
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

    def arc(self, start_x, start_y, diameter) -> List[Tuple[Decimal, Decimal]]:
        points = []
        for i in range(0, 180, 2):
            x = math.sin(math.radians(i - 90)) * diameter
            y = math.cos(math.radians(i - 90)) * diameter
            points.append((x + start_x, y + start_y))
        return points
