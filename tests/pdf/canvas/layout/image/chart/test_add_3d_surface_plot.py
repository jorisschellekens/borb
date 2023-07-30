import unittest

import matplotlib.pyplot as MatPlotLibPlot
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


class TestAdd3DSurfacePlot(TestCase):
    """
    This test creates a PDF with a 3D surface plot in it.
    """

    @staticmethod
    def _create_plot_001() -> None:
        MatPlotLibPlot.clf()
        MatPlotLibPlot.close()
        # Get the data (csv file is hosted on the web)
        url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/volcano.csv"
        data = pd.read_csv(url)

        # Transform it to a long format
        df = data.unstack().reset_index()
        df.columns = ["X", "Y", "Z"]

        # And transform the old column name in something numeric
        df["X"] = pd.Categorical(df["X"])
        df["X"] = df["X"].cat.codes

        # We are going to do 20 plots, for 20 different angles
        for angle in range(70, 210, 2):

            # Make the plot
            fig = MatPlotLibPlot.figure(dpi=600)
            ax = fig.add_subplot(projection="3d")
            ax.plot_trisurf(df["Y"], df["X"], df["Z"], cmap="Blues", linewidth=0.2)

            # Set the angle of the camera
            ax.view_init(30, angle)

        return MatPlotLibPlot.gcf()

    SURFACE_PLOT: Chart = Chart(
        _create_plot_001(),
        width=Decimal(64),
        height=Decimal(64),
    )

    def test_add_3d_surface_plot(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF."
            )
        )
        layout.add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file(), 0.00065)

    def test_add_3d_surface_plot_using_borders(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using non-default borders."
            )
        )
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_top = True
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_right = True
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_bottom = True
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_left = True
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_color = HexColor("56cbf9")
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_radius_top_left = Decimal(10)
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_radius_top_right = Decimal(10)
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_radius_bottom_right = Decimal(10)
        layout.add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file(), 0.00065)
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_top = False
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_right = False
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_bottom = False
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_left = False
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_color = HexColor("000000")
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_radius_top_left = Decimal(0)
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_radius_top_right = Decimal(0)
        TestAdd3DSurfacePlot.SURFACE_PLOT._border_radius_bottom_right = Decimal(0)

    def test_add_3d_surface_plot_using_horizontal_align_left(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to LEFT."
            )
        )
        TestAdd3DSurfacePlot.SURFACE_PLOT._horizontal_alignment = Alignment.LEFT
        layout.add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file(), 0.00065)
        TestAdd3DSurfacePlot.SURFACE_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_3d_surface_plot_using_horizontal_alignment_centered(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to CENTERED."
            )
        )
        TestAdd3DSurfacePlot.SURFACE_PLOT._horizontal_alignment = Alignment.CENTERED
        layout.add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file(), 0.00065)
        TestAdd3DSurfacePlot.SURFACE_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_3d_surface_plot_using_horizontal_alignment_right(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to RIGHT."
            )
        )
        TestAdd3DSurfacePlot.SURFACE_PLOT._horizontal_alignment = Alignment.RIGHT
        layout.add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file(), 0.00065)
        TestAdd3DSurfacePlot.SURFACE_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_orderedlist_of_3d_surface_plots(self):
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
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        )
        with open(self.get_sixth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_sixth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixth_output_file(), 0.00065)

    def test_add_unorderedlist_of_3d_surface_plots(self):
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
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        )
        with open(self.get_seventh_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_seventh_output_file())
        self.compare_visually_to_ground_truth(self.get_seventh_output_file(), 0.00065)

    def test_add_table_of_3d_surface_plots(self):
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
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
            .add(TestAdd3DSurfacePlot.SURFACE_PLOT)
        )
        with open(self.get_eight_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_eight_output_file())
        self.compare_visually_to_ground_truth(self.get_eight_output_file(), 0.00065)


if __name__ == "__main__":
    unittest.main()
