import unittest
from datetime import datetime
from math import pi
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
from tests.test_util import compare_visually_to_ground_truth


class TestWriteRadarPlot(unittest.TestCase):
    """
    This test creates a PDF with a radar plot in it.
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
            .add(Paragraph("This test creates a PDF with a radar plot in it."))
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

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf", 0.0004)


if __name__ == "__main__":
    unittest.main()
