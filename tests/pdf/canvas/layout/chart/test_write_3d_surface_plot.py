import logging
import unittest
from pathlib import Path

import matplotlib.pyplot as MatPlotLibPlot
import pandas as pd

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.chart import Chart
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Heading, Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-3d-surface-chart.log", level=logging.DEBUG
)


class TestWriteBasic3DChart(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-write-3d-surface-chart")

    def _create_plot(self) -> None:
        # Get the data (csv file is hosted on the web)
        url = "https://python-graph-gallery.com/wp-content/uploads/volcano.csv"
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
            fig = MatPlotLibPlot.figure()
            ax = fig.gca(projection="3d")
            ax.plot_trisurf(
                df["Y"], df["X"], df["Z"], cmap=MatPlotLibPlot.cm.viridis, linewidth=0.2
            )

            # Set the angle of the camera
            ax.view_init(30, angle)

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
            Heading("3D Plot", font_color=X11Color("Orange"), font_size=Decimal(20))
        )
        layout.add(
            Paragraph(
                "Demonstrates plotting a 3D surface colored with the coolwarm color map. "
                "The surface can be made opaque by using antialiased=False."
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
                stroke_color=X11Color("Orange"),
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
