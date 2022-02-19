import unittest
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as MatPlotLibPlot

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWrite2ScatterPlots(unittest.TestCase):
    """
    This test creates a PDF with 2 scatter plots in it.
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
            .add(Paragraph("This test creates a PDF with 2 scatter plots in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add chart
        import numpy as np

        # create data
        x = np.random.rand(15)
        y = x + np.random.rand(15)
        z = x + np.random.rand(15)
        z = z * z

        # scatter plot 1
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
        layout.add(
            Chart(
                MatPlotLibPlot.gcf(),
                width=Decimal(256),
                height=Decimal(256),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # scatter plot 2
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
        layout.add(
            Chart(
                MatPlotLibPlot.gcf(),
                width=Decimal(256),
                height=Decimal(256),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
