import logging
import math
from decimal import Decimal
from pathlib import Path
from typing import Tuple, List

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../../logs/test-add-polyline-annotation.log", level=logging.DEBUG
)


class TestAddPolylineAnnotation(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../output/test-add-polyline-annotation")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_corpus(self):
        super(TestAddPolylineAnnotation, self).test_corpus()

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
        for i, color in enumerate(
            [
                X11Color("Red"),
                X11Color("Orange"),
                X11Color("Yellow"),
                X11Color("Green"),
                X11Color("Blue"),
                X11Color("Violet"),
            ]
        ):
            doc.get_page(0).append_polyline_annotation(
                points=self.arc(200 + 4 * i, 200, 64 - 2 * i),
                stroke_color=color,
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
