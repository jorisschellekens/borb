import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestAddPolylineAnnotationUsingLineArtFactory(unittest.TestCase):
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

    def test_add_line_art_annotation(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and all line art annotations."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        shapes = [
            LineArtFactory.cartoon_diamond(
                Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.isosceles_triangle(
                Rectangle(Decimal(110), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.parallelogram(
                Rectangle(Decimal(220), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.trapezoid(
                Rectangle(Decimal(330), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.diamond(
                Rectangle(Decimal(440), Decimal(0), Decimal(100), Decimal(100))
            ),
            # second row
            LineArtFactory.pentagon(
                Rectangle(Decimal(0), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.hexagon(
                Rectangle(Decimal(110), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.heptagon(
                Rectangle(Decimal(220), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.octagon(
                Rectangle(Decimal(330), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.regular_n_gon(
                Rectangle(Decimal(440), Decimal(110), Decimal(100), Decimal(100)), 17
            ),
            # third row
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(0), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.25),
            ),
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(110), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.33),
            ),
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(220), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.5),
            ),
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(330), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.75),
            ),
            LineArtFactory.droplet(
                Rectangle(Decimal(440), Decimal(220), Decimal(100), Decimal(100))
            ),
            # fourth row
            LineArtFactory.four_pointed_star(
                Rectangle(Decimal(0), Decimal(330), Decimal(100), Decimal(100))
            ),
            LineArtFactory.five_pointed_star(
                Rectangle(Decimal(110), Decimal(330), Decimal(100), Decimal(100))
            ),
            LineArtFactory.six_pointed_star(
                Rectangle(Decimal(220), Decimal(330), Decimal(100), Decimal(100))
            ),
            LineArtFactory.n_pointed_star(
                Rectangle(Decimal(330), Decimal(330), Decimal(100), Decimal(100)), 8
            ),
            LineArtFactory.n_pointed_star(
                Rectangle(Decimal(440), Decimal(330), Decimal(100), Decimal(100)), 10
            ),
            # fifth row
            LineArtFactory.arrow_left(
                Rectangle(Decimal(0), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.arrow_right(
                Rectangle(Decimal(110), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.arrow_up(
                Rectangle(Decimal(220), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.arrow_down(
                Rectangle(Decimal(330), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.sticky_note(
                Rectangle(Decimal(440), Decimal(440), Decimal(100), Decimal(100))
            ),
        ]

        colors = [
            HexColor("f1cd2e"),
            HexColor("56CBF9"),
            HexColor("0B3954"),
            HexColor("f1cd2e"),
        ]

        # add annotation
        for i, s in enumerate(shapes):
            pdf.get_page(0).append_polyline_annotation(
                points=s,
                fill_color=colors[(i + 1) % len(colors)],
                stroke_color=colors[i % len(colors)],
            )

        # attempt to store PDF
        with open(self.output_dir / "output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

        # attempt to re-open PDF
        with open(self.output_dir / "output.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        return True
