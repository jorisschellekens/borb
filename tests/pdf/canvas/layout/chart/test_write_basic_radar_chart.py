import logging
import unittest
from math import pi
from pathlib import Path

import matplotlib.pyplot as MatPlotLibPlot
import pandas as pd

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.barcode import BarcodeType, Barcode
from ptext.pdf.canvas.layout.chart import Chart
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Heading, Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-basic-radar-chart.log", level=logging.DEBUG
)


class TestWriteBasicRadarChart(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-write-basic-radar-chart")

    def _create_plot(self) -> None:
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
        values

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

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # set layout
        layout = MultiColumnLayout(page)

        # add chart
        layout.add(Chart(self._create_plot()))

        layout.switch_to_next_column()

        # add Heading
        layout.add(
            Heading(
                "Basic Radar Chart",
                font_color=X11Color("SteelBlue"),
                font_size=Decimal(20),
            )
        )
        layout.add(
            Paragraph(
                "A radar chart displays the value of several numerical variables for one or several entities. "
                "Here is an example of a simple one, displaying the values of 5 variables for only one individual."
            )
        )
        layout.add(
            Paragraph(
                "To my knowledge, there is no built in function allowing to make radar charts with Matplotlib. "
                "Thus, we have to use basic functions to build it, what makes it a bit fastidious."
            )
        )
        layout.add(
            Paragraph(
                "Check out https://python-graph-gallery.com/ for more wonderful examples of plots in Python."
            )
        )
        layout.add(
            Barcode(
                data="https://python-graph-gallery.com/",
                type=BarcodeType.QR,
                stroke_color=X11Color("SteelBlue"),
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
