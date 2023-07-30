import unittest

import matplotlib.pyplot as MatPlotLibPlot
import numpy as np
import pandas as pd

from borb.io.read.types import Decimal
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import OrderedList
from borb.pdf import UnorderedList
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAdd3DDensityPlot(TestCase):
    """
    This test creates a PDF with a 3D density plot in it.
    """

    @staticmethod
    def _create_plot_001() -> None:
        MatPlotLibPlot.clf()
        MatPlotLibPlot.close()
        # Dataset
        np.random.seed(1024)
        df = pd.DataFrame(
            {
                "X": range(1, 101),
                "Y": np.random.randn(100) * 15 + range(1, 101),
                "Z": (np.random.randn(100) * 15 + range(1, 101)) * 2,
            }
        )
        fig = MatPlotLibPlot.figure(dpi=600)
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(df["X"], df["Y"], df["Z"], c="#56cbf9", s=60)
        ax.view_init(30, 185)
        return MatPlotLibPlot.gcf()

    DENSITY_PLOT: Chart = Chart(
        _create_plot_001(), width=Decimal(64), height=Decimal(64)
    )

    def test_add_3d_density_plot(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF."
            )
        )
        layout.add(TestAdd3DDensityPlot.DENSITY_PLOT)
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file(), 0.00065)

    def test_add_3d_density_plot_using_borders(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using non-default borders."
            )
        )
        TestAdd3DDensityPlot.DENSITY_PLOT._border_top = True
        TestAdd3DDensityPlot.DENSITY_PLOT._border_right = True
        TestAdd3DDensityPlot.DENSITY_PLOT._border_bottom = True
        TestAdd3DDensityPlot.DENSITY_PLOT._border_left = True
        TestAdd3DDensityPlot.DENSITY_PLOT._border_color = HexColor("56cbf9")
        TestAdd3DDensityPlot.DENSITY_PLOT._border_radius_top_left = Decimal(10)
        TestAdd3DDensityPlot.DENSITY_PLOT._border_radius_top_right = Decimal(10)
        TestAdd3DDensityPlot.DENSITY_PLOT._border_radius_bottom_right = Decimal(10)
        layout.add(TestAdd3DDensityPlot.DENSITY_PLOT)
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file(), 0.00065)

        TestAdd3DDensityPlot.DENSITY_PLOT._border_top = False
        TestAdd3DDensityPlot.DENSITY_PLOT._border_right = False
        TestAdd3DDensityPlot.DENSITY_PLOT._border_bottom = False
        TestAdd3DDensityPlot.DENSITY_PLOT._border_left = False
        TestAdd3DDensityPlot.DENSITY_PLOT._border_color = HexColor("000000")
        TestAdd3DDensityPlot.DENSITY_PLOT._border_radius_top_left = Decimal(0)
        TestAdd3DDensityPlot.DENSITY_PLOT._border_radius_top_right = Decimal(0)
        TestAdd3DDensityPlot.DENSITY_PLOT._border_radius_bottom_right = Decimal(0)

    def test_add_3d_density_plot_using_horizontal_align_left(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to LEFT."
            )
        )
        TestAdd3DDensityPlot.DENSITY_PLOT._horizontal_alignment = Alignment.LEFT
        layout.add(TestAdd3DDensityPlot.DENSITY_PLOT)
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file(), 0.00065)
        TestAdd3DDensityPlot.DENSITY_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_3d_density_plot_using_horizontal_alignment_centered(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to CENTERED."
            )
        )
        TestAdd3DDensityPlot.DENSITY_PLOT._horizontal_alignment = Alignment.CENTERED
        layout.add(TestAdd3DDensityPlot.DENSITY_PLOT)
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file(), 0.00065)
        TestAdd3DDensityPlot.DENSITY_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_3d_density_plot_using_horizontal_alignment_right(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to RIGHT."
            )
        )
        TestAdd3DDensityPlot.DENSITY_PLOT._horizontal_alignment = Alignment.RIGHT
        layout.add(TestAdd3DDensityPlot.DENSITY_PLOT)
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file(), 0.00065)
        TestAdd3DDensityPlot.DENSITY_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_orderedlist_of_3d_density_plots(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds an OrderedList of MatPlotLib charts to a PDF."
            )
        )
        layout.add(
            OrderedList()
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
        )
        with open(self.get_sixth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_sixth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixth_output_file(), 0.00065)

    def test_add_unorderedlist_of_3d_density_plots(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds an UnorderedList of MatPlotLib charts to a PDF."
            )
        )
        layout.add(
            UnorderedList()
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
        )
        with open(self.get_seventh_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_seventh_output_file())
        self.compare_visually_to_ground_truth(self.get_seventh_output_file(), 0.00065)

    def test_add_table_of_3d_density_plots(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a Table of MatPlotLib charts to a PDF."
            )
        )
        layout.add(
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
            .add(TestAdd3DDensityPlot.DENSITY_PLOT)
        )
        with open(self.get_eight_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_eight_output_file())
        self.compare_visually_to_ground_truth(self.get_eight_output_file(), 0.00065)


if __name__ == "__main__":
    unittest.main()
