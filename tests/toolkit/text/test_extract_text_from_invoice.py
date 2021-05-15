import typing
import unittest
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.font.font import Font

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.pdf import PDF
from ptext.toolkit.location.location_filter import LocationFilter
from ptext.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from ptext.toolkit.text.simple_text_extraction import SimpleTextExtraction
from tests.util import get_output_dir


class TestExtractTextFromInvoice(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-extract-text-from-invoice")
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_extract_all_text(self):
        l = SimpleTextExtraction()
        with open(
            Path("/home/joris/Code/pdf-corpus/0600.pdf"), "rb"
        ) as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l])
        print(l.get_text(0))

    def test_extract_text_in_area(self):
        r = Rectangle(Decimal(50), Decimal(400), Decimal(200), Decimal(100))
        doc = None
        file: Path = Path("/home/joris/Code/pdf-corpus/0600.pdf")
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        output_file = self.output_dir / (file.stem + "_bill_to_marked.pdf")
        with open(output_file, "wb") as pdf_file_handle:
            doc.get_page(0).append_polygon_annotation(
                LineArtFactory.rectangle(r),
                stroke_color=X11Color("Red"),
            )
            PDF.dumps(pdf_file_handle, doc)

        l1 = SimpleTextExtraction()
        l2 = LocationFilter(
            r.get_x(), r.get_y(), r.get_x() + r.get_width(), r.get_y() + r.get_height()
        ).add_listener(l1)

        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l2])

        print(l1.get_text(0))

    def bounding_box(self, rectangles: typing.List[Rectangle]) -> Rectangle:
        min_x: Decimal = rectangles[0].get_x()
        min_y: Decimal = rectangles[1].get_y()
        max_x: Decimal = rectangles[0].get_x() + rectangles[0].get_width()
        max_y: Decimal = rectangles[1].get_y() + rectangles[0].get_height()
        for r in rectangles:
            min_x = min(min_x, r.get_x())
            min_y = min(min_y, r.get_y())
            max_x = max(max_x, r.get_x() + r.get_width())
            max_y = max(max_y, r.get_y() + r.get_height())
        w: Decimal = max_x - min_x
        h: Decimal = max_y - min_y
        return Rectangle(min_x, min_y, w, h)

    def test_extract_text_with_regex(self):

        l = RegularExpressionTextExtraction("[dD]ue [dD]ate [0-9]+/[0-9]+/[0-9]+")
        file: Path = Path("/home/joris/Code/pdf-corpus/0600.pdf")
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l])

        bounding_box: typing.Optional[Rectangle] = None
        output_file = self.output_dir / (file.stem + "_due_date_marked.pdf")
        with open(output_file, "wb") as pdf_file_handle:
            rects: typing.List[Rectangle] = [
                x.get_bounding_box()
                for x in l.get_matched_chunk_of_text_render_events_per_page(0)
            ]
            bounding_box = self.bounding_box(rects)
            doc.get_page(0).append_polygon_annotation(
                LineArtFactory.rectangle(bounding_box),
                stroke_color=X11Color("Red"),
            )
            PDF.dumps(pdf_file_handle, doc)

        # expand box a bit
        if bounding_box:
            p = Decimal(2)
            bounding_box = Rectangle(
                bounding_box.get_x() - p,
                bounding_box.get_y() - p,
                bounding_box.get_width() + 2 * p,
                bounding_box.get_height() + 2 * p,
            )

        l1 = SimpleTextExtraction()
        l2 = LocationFilter(
            bounding_box.get_x(),
            bounding_box.get_y(),
            bounding_box.get_x() + bounding_box.get_width(),
            bounding_box.get_y() + bounding_box.get_height(),
        ).add_listener(l1)

        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l2])

        print(l1.get_text(0))
