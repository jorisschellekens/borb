import logging
import unittest
from pathlib import Path

from ptext.pdf.canvas.layout.shape import Shape

from ptext.pdf.canvas.layout.page_layout import SingleColumnLayout

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import Paragraph, Alignment
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-flowchart-line-art.log"),
    level=logging.DEBUG,
)


class TestWriteFlowchartLineArt(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-flowchart-line-art")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)

        # title
        layout.add(
            Paragraph(
                "Flowchart Line Art", font_size=Decimal(20), font_color=X11Color("Blue")
            )
        )

        # table
        fixed_bb = Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100))
        t = Table(number_of_rows=10, number_of_columns=6)
        t.add(
            Shape(
                LineArtFactory.flowchart_process(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_decision(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_document(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_predefined_document(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                # LineArtFactory.flowchart_multiple_documents(fixed_bb)
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_data(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
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
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                # LineArtFactory.flowchart_stored_data(fixed_bb),
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_internal_storage(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_sequential_data(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                # LineArtFactory.flowchart_direct_data(fixed_bb),
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_manual_input(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
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
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_card(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_paper_tape(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                # LineArtFactory.flowchart_display(fixed_bb),
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_preparation(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_loop_limit(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
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
                # LineArtFactory.flowchart_termination(fixed_bb),
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_collate(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                # LineArtFactory.flowchart_delay(fixed_bb),
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_extract(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_merge(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_or(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
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
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_summing_junction(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.regular_n_gon(fixed_bb, 8),
                # LineArtFactory.flowchart_database(fixed_bb),
                fill_color=X11Color("White"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_on_page_reference(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_off_page_reference(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
            )
        )
        t.add(
            Shape(
                LineArtFactory.flowchart_process_iso_9000(fixed_bb),
                fill_color=X11Color("Blue"),
                stroke_color=X11Color("Black"),
                line_width=Decimal(1),
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
