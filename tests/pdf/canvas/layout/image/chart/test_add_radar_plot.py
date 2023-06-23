import unittest
from math import pi

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


class TestAddRadarPlot(TestCase):
    """
    This test creates a PDF with a radar plot in it.
    """

    @staticmethod
    def _create_plot_001() -> None:
        MatPlotLibPlot.clf()
        MatPlotLibPlot.close()
        df = pd.DataFrame(
            {
                "group": ["A", "B", "C", "D"],
                "var1": [38, 1.5, 30, 4],
                "var2": [29, 10, 9, 34],
                "var3": [8, 39, 23, 24],
                "var4": [7, 31, 33, 14],
                "var5": [28, 15, 32, 14],
            }
        )

        # number of variable
        categories = list(df)[1:]
        N = len(categories)

        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        values = df.loc[0].drop("group").values.flatten().tolist()
        values += values[:1]

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = MatPlotLibPlot.subplot(111, polar=True)

        # Draw one axe per variable + add labels labels yet
        MatPlotLibPlot.xticks(angles[:-1], categories, color="grey", size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
        MatPlotLibPlot.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
        MatPlotLibPlot.ylim(0, 40)

        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle="solid")

        # Fill area
        ax.fill(angles, values, "b", alpha=0.1)

        return MatPlotLibPlot.gcf()

    RADAR_PLOT: Chart = Chart(_create_plot_001(), width=Decimal(64), height=Decimal(64))

    def test_add_radar_plot(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF."
            )
        )
        layout.add(TestAddRadarPlot.RADAR_PLOT)
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file(), 0.00065)

    def test_add_radar_plot_using_borders(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using non-default borders."
            )
        )

        TestAddRadarPlot.RADAR_PLOT._border_top = True
        TestAddRadarPlot.RADAR_PLOT._border_right = True
        TestAddRadarPlot.RADAR_PLOT._border_bottom = True
        TestAddRadarPlot.RADAR_PLOT._border_left = True
        TestAddRadarPlot.RADAR_PLOT._border_color = HexColor("56cbf9")
        TestAddRadarPlot.RADAR_PLOT._border_radius_top_left = Decimal(10)
        TestAddRadarPlot.RADAR_PLOT._border_radius_top_right = Decimal(10)
        TestAddRadarPlot.RADAR_PLOT._border_radius_bottom_right = Decimal(10)

        layout.add(TestAddRadarPlot.RADAR_PLOT)
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file(), 0.00065)

        TestAddRadarPlot.RADAR_PLOT._border_top = False
        TestAddRadarPlot.RADAR_PLOT._border_right = False
        TestAddRadarPlot.RADAR_PLOT._border_bottom = False
        TestAddRadarPlot.RADAR_PLOT._border_left = False
        TestAddRadarPlot.RADAR_PLOT._border_color = HexColor("000000")
        TestAddRadarPlot.RADAR_PLOT._border_radius_top_left = Decimal(0)
        TestAddRadarPlot.RADAR_PLOT._border_radius_top_right = Decimal(0)
        TestAddRadarPlot.RADAR_PLOT._border_radius_bottom_right = Decimal(0)

    def test_add_radar_plot_using_horizontal_align_left(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to LEFT."
            )
        )
        TestAddRadarPlot.RADAR_PLOT._horizontal_alignment = Alignment.LEFT
        layout.add(TestAddRadarPlot.RADAR_PLOT)
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file(), 0.00065)
        TestAddRadarPlot.RADAR_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_radar_plot_using_horizontal_alignment_centered(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to CENTERED."
            )
        )
        TestAddRadarPlot.RADAR_PLOT._horizontal_alignment = Alignment.CENTERED
        layout.add(TestAddRadarPlot.RADAR_PLOT)
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file(), 0.00065)
        TestAddRadarPlot.RADAR_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_radar_plot_using_horizontal_alignment_right(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a MatPlotLib chart to a PDF using horizontal align set to RIGHT."
            )
        )
        TestAddRadarPlot.RADAR_PLOT._horizontal_alignment = Alignment.RIGHT
        layout.add(TestAddRadarPlot.RADAR_PLOT)
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file(), 0.00065)
        TestAddRadarPlot.RADAR_PLOT._horizontal_alignment = Alignment.LEFT

    def test_add_orderedlist_of_radar_plots(self):
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
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
        )
        with open(self.get_sixth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_sixth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixth_output_file(), 0.00065)

    def test_add_unorderedlist_of_radar_plots(self):
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
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
        )
        with open(self.get_seventh_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_seventh_output_file())
        self.compare_visually_to_ground_truth(self.get_seventh_output_file(), 0.00065)

    def test_add_table_of_radar_plots(self):
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
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
            .add(TestAddRadarPlot.RADAR_PLOT)
        )
        with open(self.get_eight_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.check_pdf_using_validator(self.get_eight_output_file())
        self.compare_visually_to_ground_truth(self.get_eight_output_file(), 0.00065)


if __name__ == "__main__":
    unittest.main()
