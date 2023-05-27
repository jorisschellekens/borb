import math

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddDragonCurve(TestCase):
    """
    This test creates a PDF with a dragon-curve in it.
    """

    def _create_connectedshape(self, page: Page) -> ConnectedShape:
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height() - Decimal(200)
        assert w is not None
        assert h is not None
        return ConnectedShape(
            LineArtFactory.smooth_dragon_curve(
                bounding_box=Rectangle(
                    Decimal(0), Decimal(0), Decimal(200), Decimal(200)
                ),
                number_of_iterations=10,
            ),
            stroke_color=HexColor("f1cd2e"),
            line_width=Decimal(1),
            fill_color=None,
        )

    def test_add_dragon_curve_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a dragon-curve in it."
            )
        )
        layout.add(self._create_connectedshape(page))
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_dragon_curve_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a dragon-curve in it."
            )
        )
        layout.add(self._create_connectedshape(page).rotate(math.radians(45)))
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())
