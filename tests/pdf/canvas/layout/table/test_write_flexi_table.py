import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteFlexiTable(unittest.TestCase):
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

    def test_write_document_001(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # write test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a simple Table in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = FlexibleColumnWidthTable(
            number_of_rows=5,
            number_of_columns=2,
            padding_top=Decimal(5),
            horizontal_alignment=Alignment.RIGHT,
        )
        t.add(
            Paragraph(
                "Language",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Nof. Questions",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        t.add(Paragraph("Javascript"))
        t.add(Paragraph("2,167,178"))

        t.add(Paragraph("Php"))
        t.add(Paragraph("1,391,524"))

        t.add(Paragraph("C++"))
        t.add(Paragraph("711,944"))

        t.add(Paragraph("Java"))
        t.add(Paragraph("1,752,877"))
        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        layout.add(
            Paragraph(
                text="**Data gathered from Stackoverflow.com on 10th of february 2021",
                font_size=Decimal(8),
                font_color=X11Color("Gray"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_001.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

    def test_write_document_002(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # write test information
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
                    "This test creates a PDF with a simple Table in it. The Table only has outside borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = FlexibleColumnWidthTable(
            number_of_rows=5,
            number_of_columns=2,
            padding_top=Decimal(5),
            horizontal_alignment=Alignment.RIGHT,
        )
        t.add(
            Paragraph(
                "Language",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Nof. Questions",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        t.add(Paragraph("Javascript"))
        t.add(Paragraph("2,167,178"))

        t.add(Paragraph("Php"))
        t.add(Paragraph("1,391,524"))

        t.add(Paragraph("C++"))
        t.add(Paragraph("711,944"))

        t.add(Paragraph("Java"))
        t.add(Paragraph("1,752,877"))
        t.outer_borders()
        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        layout.add(
            Paragraph(
                text="**Data gathered from Stackoverflow.com on 10th of february 2021",
                font_size=Decimal(8),
                font_color=X11Color("Gray"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_002.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")

    def test_write_document_003(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # write test information
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
                    "This test creates a PDF with a simple Table in it. The table has no borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = FlexibleColumnWidthTable(
            number_of_rows=5,
            number_of_columns=2,
            padding_top=Decimal(5),
            horizontal_alignment=Alignment.RIGHT,
        )
        t.add(
            Paragraph(
                "Language",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Nof. Questions",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        t.add(Paragraph("Javascript"))
        t.add(Paragraph("2,167,178"))

        t.add(Paragraph("Php"))
        t.add(Paragraph("1,391,524"))

        t.add(Paragraph("C++"))
        t.add(Paragraph("711,944"))

        t.add(Paragraph("Java"))
        t.add(Paragraph("1,752,877"))
        t.no_borders()
        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        layout.add(
            Paragraph(
                text="**Data gathered from Stackoverflow.com on 10th of february 2021",
                font_size=Decimal(8),
                font_color=X11Color("Gray"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_003.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_003.pdf")

    def test_write_document_004(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # write test information
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
                    "This test creates a PDF with a simple Table in it. The Table only has internal borders."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = FlexibleColumnWidthTable(
            number_of_rows=5,
            number_of_columns=2,
            padding_top=Decimal(5),
            horizontal_alignment=Alignment.RIGHT,
        )
        t.add(
            Paragraph(
                "Language",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Nof. Questions",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        t.add(Paragraph("Javascript"))
        t.add(Paragraph("2,167,178"))

        t.add(Paragraph("Php"))
        t.add(Paragraph("1,391,524"))

        t.add(Paragraph("C++"))
        t.add(Paragraph("711,944"))

        t.add(Paragraph("Java"))
        t.add(Paragraph("1,752,877"))
        t.internal_borders()
        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        layout.add(
            Paragraph(
                text="**Data gathered from Stackoverflow.com on 10th of february 2021",
                font_size=Decimal(8),
                font_color=X11Color("Gray"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_004.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_004.pdf")

    def test_write_document_005(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # write test information
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
                    "This test creates a PDF with a simple Table in it. The table is striped."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t = FlexibleColumnWidthTable(
            number_of_rows=5,
            number_of_columns=2,
            padding_top=Decimal(5),
            horizontal_alignment=Alignment.RIGHT,
        )
        t.add(
            Paragraph(
                "Language",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Paragraph(
                "Nof. Questions",
                font_color=HexColor("f1cd2e"),
                font_size=Decimal(18.2),
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        t.add(Paragraph("Javascript"))
        t.add(Paragraph("2,167,178"))

        t.add(Paragraph("Php"))
        t.add(Paragraph("1,391,524"))

        t.add(Paragraph("C++"))
        t.add(Paragraph("711,944"))

        t.add(Paragraph("Java"))
        t.add(Paragraph("1,752,877"))
        t.internal_borders()
        t.even_odd_row_colors(HexColor("FFFFFF"), HexColor("d3d3d3"))
        t.set_border_width_on_all_cells(Decimal(0.2))
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))

        layout.add(t)

        layout.add(
            Paragraph(
                text="**Data gathered from Stackoverflow.com on 10th of february 2021",
                font_size=Decimal(8),
                font_color=X11Color("Gray"),
                horizontal_alignment=Alignment.RIGHT,
            )
        )

        # determine output location
        out_file = self.output_dir / ("output_005.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_005.pdf")
