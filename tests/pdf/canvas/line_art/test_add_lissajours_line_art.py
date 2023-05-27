from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddLissajours(TestCase):
    """
    This test creates a PDF with a Table of variously parametrized Lissajours figures in it.
    """

    def test_add_lissajours(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a Table of variously parametrized "
                "Lissajours figures in it."
            )
        )

        # table
        N: int = 7
        fill_colors = [HexColor("f1cd2e"), HexColor("0b3954"), HexColor("56cbf9")]
        stroke_colors = [HexColor("0b3954"), HexColor("f1cd2e"), HexColor("a5ffd6")]
        fixed_bb = Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100))
        t = Table(number_of_rows=N, number_of_columns=N, padding_top=Decimal(5))
        for i in range(0, N):
            for j in range(0, N):
                t.add(
                    ConnectedShape(
                        LineArtFactory.lissajours(fixed_bb, i + 1, j + 1),
                        fill_color=fill_colors[(i + j) % len(fill_colors)],
                        stroke_color=stroke_colors[(i + j) % len(stroke_colors)],
                        line_width=Decimal(2),
                        horizontal_alignment=Alignment.CENTERED,
                    ).scale_down(Decimal(32), Decimal(32))
                )

        t.set_padding_on_all_cells(Decimal(10), Decimal(10), Decimal(10), Decimal(10))
        layout.add(t)
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
