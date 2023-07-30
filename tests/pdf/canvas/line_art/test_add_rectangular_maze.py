import math
import random

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.line_art.rectangular_maze_factory import RectangularMazeFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddRectangularMaze(TestCase):
    """
    This test creates a PDF with a dragon-curve in it.
    """

    def _write_maze(self, width: int, height: int) -> DisconnectedShape:
        return DisconnectedShape(
            RectangularMazeFactory.rectangular_maze(width, height),
            stroke_color=HexColor("f1cd2e"),
            line_width=Decimal(1),
        )

    def test_add_rectangular_maze_001(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a square maze in it."
            )
        )
        random.seed(2048)
        layout.add(self._write_maze(20, 20))
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_rectangular_maze_002(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a square maze in it."
            )
        )
        random.seed(2048)
        layout.add(self._write_maze(10, 20))
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_rectangular_maze_003(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a square maze in it."
            )
        )
        random.seed(2048)
        layout.add(self._write_maze(20, 10))
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_rectangular_maze_004(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a square maze in it."
            )
        )
        random.seed(2048)
        layout.add(self._write_maze(20, 20).rotate(math.radians(45)))
        with open(self.get_fourth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())
