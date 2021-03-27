import logging
import unittest
from pathlib import Path

import matplotlib.pyplot as MatPlotLibPlot
import numpy as np
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
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-3d-density-chart.log"), level=logging.DEBUG
)


class TestWriteBasicRadarChart(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-3d-density-chart")

    def _create_plot(self) -> None:
        # Dataset
        df = pd.DataFrame(
            {
                "X": range(1, 101),
                "Y": np.random.randn(100) * 15 + range(1, 101),
                "Z": (np.random.randn(100) * 15 + range(1, 101)) * 2,
            }
        )

        # plot
        fig = MatPlotLibPlot.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(df["X"], df["Y"], df["Z"], c="skyblue", s=60)
        ax.view_init(30, 185)

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
                "3D Density Chart",
                font_color=X11Color("YellowGreen"),
                font_size=Decimal(20),
            )
        )
        layout.add(
            Paragraph(
                "The mplot3D toolkit of Matplotlib allows to easily create 3D scatterplots. "
                "Note that most of the customisations presented in the Scatterplot section will work in 3D as well. "
                "The result can be a bit disappointing since each marker is represented as a dot, not as a sphere.."
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
                stroke_color=X11Color("YellowGreen"),
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
