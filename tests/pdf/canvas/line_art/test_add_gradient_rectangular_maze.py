import random

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.layout.shape.gradient_colored_disconnected_shape import (
    GradientColoredDisconnectedShape,
)
from borb.pdf.canvas.line_art.rectangular_maze_factory import RectangularMazeFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddGradientRectangularMaze(TestCase):
    """
    This test creates a PDF with a dragon-curve in it.
    """

    def _create_gradientcoloreddisconnectedshape(
        self,
        gradient_type: GradientColoredDisconnectedShape.GradientType,
    ):
        return GradientColoredDisconnectedShape(
            DisconnectedShape(
                RectangularMazeFactory.rectangular_maze(20, 20),
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
                stroke_color=HexColor("f1cd2e"),
                line_width=Decimal(1),
            ),
            from_color=HexColor("ff0000"),
            to_color=HexColor("0000ff"),
            gradient_type=gradient_type,
        )

    def test_add_gradientcoloreddisconnectedshape_001(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a GradientColoredDisconnectedShape in it."
            )
        )

        random.seed(2048)
        layout.add(
            self._create_gradientcoloreddisconnectedshape(
                gradient_type=GradientColoredDisconnectedShape.GradientType.DIAGONAL
            )
        )

        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_gradientcoloreddisconnectedshape_002(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a GradientColoredDisconnectedShape in it."
            )
        )

        random.seed(2048)
        layout.add(
            self._create_gradientcoloreddisconnectedshape(
                gradient_type=GradientColoredDisconnectedShape.GradientType.HORIZONTAL
            )
        )

        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_gradientcoloreddisconnectedshape_003(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a GradientColoredDisconnectedShape in it."
            )
        )

        random.seed(2048)
        layout.add(
            self._create_gradientcoloreddisconnectedshape(
                gradient_type=GradientColoredDisconnectedShape.GradientType.RADIAL
            )
        )

        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_gradientcoloreddisconnectedshape_004(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a GradientColoredDisconnectedShape in it."
            )
        )

        random.seed(2048)
        layout.add(
            self._create_gradientcoloreddisconnectedshape(
                gradient_type=GradientColoredDisconnectedShape.GradientType.VERTICAL
            )
        )

        with open(self.get_fourth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())
