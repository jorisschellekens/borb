import unittest
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as MatPlotLibPlot
import pandas as pd

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWrite3DSurfacePlot(unittest.TestCase):
    """
    This test creates a PDF with a 3D surface plot in it.
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
            fig = MatPlotLibPlot.figure()
            ax = fig.gca(projection="3d")
            ax.plot_trisurf(
                df["Y"], df["X"], df["Z"], cmap=MatPlotLibPlot.cm.viridis, linewidth=0.2
            )

            # Set the angle of the camera
            ax.view_init(30, angle)

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
            .add(Paragraph("This test creates a PDF with a 3D surface plot in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add chart
        layout.add(
            Chart(
                self._create_plot(),
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
