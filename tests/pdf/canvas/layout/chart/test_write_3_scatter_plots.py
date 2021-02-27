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

logging.basicConfig(
    filename="../../../../logs/test-write-3-scatter-plots.log", level=logging.DEBUG
)


class TestWrite3ScatterPlots(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-write-3-scatter-plots")

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
        from matplotlib import pyplot as plt
        import numpy as np

        # create data
        x = np.random.rand(15)
        y = x + np.random.rand(15)
        z = x + np.random.rand(15)
        z = z * z

        layout.add(
            Heading(
                "#197 Available color palettes with Matplotlib",
                font_size=Decimal(20),
                font_color=X11Color("SteelBlue"),
            )
        )

        # Use it with a call in cmap
        layout.add(
            Heading(
                "1.0 BuPu",
                font_size=Decimal(16),
                font_color=X11Color("DarkBlue"),
                outline_level=1,
            )
        )
        MatPlotLibPlot.scatter(
            x,
            y,
            s=z * 2000,
            c=x,
            cmap="BuPu",
            alpha=0.4,
            edgecolors="grey",
            linewidth=2,
        )
        layout.add(Chart(MatPlotLibPlot.gcf()))

        # You can reverse it:
        layout.add(
            Heading(
                "1.1 Inferno",
                font_size=Decimal(16),
                font_color=X11Color("DarkBlue"),
                outline_level=1,
            )
        )
        MatPlotLibPlot.scatter(
            x,
            y,
            s=z * 2000,
            c=x,
            cmap="inferno",
            alpha=0.4,
            edgecolors="grey",
            linewidth=2,
        )
        layout.add(Chart(MatPlotLibPlot.gcf()))

        # add explanation
        layout.switch_to_next_column()
        layout.add(
            Paragraph(
                "Post #196 describes how to pick up a single color when working with python and matplotlib. "
                "This post aims to describe a few color palette that are provided, and thus make your life easier when plotting several color. "
                "There are 3 types of color palettes: Sequential, Discrete and Diverging. Here are a few explanations for each:"
            )
        )

        # OTHER: viridis / inferno / plasma / magma
        layout.add(
            Heading(
                "1.2 Plasma",
                font_size=Decimal(16),
                font_color=X11Color("DarkBlue"),
                outline_level=1,
            )
        )
        MatPlotLibPlot.scatter(
            x,
            y,
            s=z * 2000,
            c=x,
            cmap="plasma",
            alpha=0.4,
            edgecolors="grey",
            linewidth=2,
        )
        layout.add(Chart(MatPlotLibPlot.gcf()))

        layout.add(
            Heading(
                "2.0 Acknowledgements",
                font_size=Decimal(16),
                font_color=X11Color("DarkBlue"),
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
