import unittest
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as MatPlotLibPlot
import numpy as np
import pandas as pd
from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.image.chart import Chart
from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestWrite3DDensityChart(unittest.TestCase):
    """
    This test creates a PDF with a 3D density plot in it.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

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

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # set layout
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a 3D density plot in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add chart
        layout.add(Chart(self._create_plot()))

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
