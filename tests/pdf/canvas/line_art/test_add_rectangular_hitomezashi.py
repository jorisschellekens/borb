import math

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.line_art.rectangular_hitomezashi import RectangularHitomezashi
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddRectangularHitomezashi(TestCase):
    """
    This test creates a PDF with a dragon-curve in it.
    """

    def _create_disconnectedshape(self) -> DisconnectedShape:
        f0 = [
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            True,
        ]
        f1 = [
            False,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
        ]
        return DisconnectedShape(
            RectangularHitomezashi.hitomezashi(f0, f1),
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            stroke_color=HexColor("f1cd2e"),
            line_width=Decimal(1),
        )

    def test_add_rectangular_hitomezashi_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a rectangular hitomezashi shape in it."
            )
        )
        layout.add(self._create_disconnectedshape())
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_rectangular_hitomezashi_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a rectangular hitomezashi shape in it."
            )
        )
        layout.add(self._create_disconnectedshape().rotate(math.radians(45)))
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())
