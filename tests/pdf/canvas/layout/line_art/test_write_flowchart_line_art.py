import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.shape import Shape
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteFlowchartLineArt(unittest.TestCase):
    """
    This test creates a PDF with all (available) flowchart line-art in it.
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

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        # write test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with all (available) flowchart line-art in it."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # table
        fixed_bb = Rectangle(Decimal(0), Decimal(0), Decimal(32), Decimal(32))
        t = Table(number_of_rows=10, number_of_columns=6, margin_top=Decimal(12))
        t.add(
            Shape(
                LineArtFactory.flowchart_process(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_decision(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_document(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_predefined_document(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(Paragraph(" "))
        t.add(
            Shape(
                LineArtFactory.flowchart_data(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Process"))
        t.add(Paragraph("Decision"))
        t.add(Paragraph("Document"))
        t.add(Paragraph("Predefined Document"))
        t.add(Paragraph("Multiple Documents"))
        t.add(Paragraph("Data"))

        # second row of shapes
        t.add(
            Shape(
                LineArtFactory.flowchart_predefined_process(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_stored_data(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_internal_storage(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_sequential_data(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(Paragraph(" "))
        t.add(
            Shape(
                LineArtFactory.flowchart_manual_input(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Predefined Process"))
        t.add(Paragraph("Stored Data"))
        t.add(Paragraph("Internal Storage"))
        t.add(Paragraph("Sequential Data"))
        t.add(Paragraph("Direct Data"))
        t.add(Paragraph("Manual Input"))

        # third row of shapes
        t.add(
            Shape(
                LineArtFactory.flowchart_manual_operation(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_card(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_paper_tape(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_display(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_preparation(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_loop_limit(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Manual Operation"))
        t.add(Paragraph("Card"))
        t.add(Paragraph("Paper Tape"))
        t.add(Paragraph("Display"))
        t.add(Paragraph("Preparation"))
        t.add(Paragraph("Loop Limit"))

        # fourth row of shapes
        t.add(
            Shape(
                LineArtFactory.flowchart_termination(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_collate(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_delay(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_extract(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_merge(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_or(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Termination"))
        t.add(Paragraph("Collate"))
        t.add(Paragraph("Delay"))
        t.add(Paragraph("Extract"))
        t.add(Paragraph("Merge"))
        t.add(Paragraph("Or"))

        # fifth row of shapes
        t.add(
            Shape(
                LineArtFactory.flowchart_sort(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_summing_junction(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_database(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_on_page_reference(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_off_page_reference(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_process_iso_9000(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Sort"))
        t.add(Paragraph("Summing Junction"))
        t.add(Paragraph("Database"))
        t.add(Paragraph("On Page Reference"))
        t.add(Paragraph("Off Page Reference"))
        t.add(Paragraph("Process ISO 9000"))

        t.set_padding_on_all_cells(Decimal(10), Decimal(10), Decimal(10), Decimal(10))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output.pdf")
