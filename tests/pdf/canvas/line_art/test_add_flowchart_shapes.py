from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddFlowchartShapes(TestCase):
    """
    This test creates a PDF with all (available) flowchart line-art in it.
    """

    def test_add_flowchart_shapes(self):

        # create document
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with all (available) flowchart line-art in it."
            )
        )

        # table
        fixed_bb = Rectangle(Decimal(0), Decimal(0), Decimal(32), Decimal(32))
        t = Table(number_of_rows=10, number_of_columns=6, margin_top=Decimal(12))
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_process(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_decision(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_document(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_predefined_document(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(Paragraph(" "))
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_data(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Process", font_size=Decimal(10)))
        t.add(Paragraph("Decision", font_size=Decimal(10)))
        t.add(Paragraph("Document", font_size=Decimal(10)))
        t.add(Paragraph("Predefined Document", font_size=Decimal(10)))
        t.add(Paragraph("Multiple Documents", font_size=Decimal(10)))
        t.add(Paragraph("Data", font_size=Decimal(10)))

        # second row of shapes
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_predefined_process(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_stored_data(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_internal_storage(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_sequential_data(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(Paragraph(" "))
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_manual_input(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Predefined Process", font_size=Decimal(10)))
        t.add(Paragraph("Stored Data", font_size=Decimal(10)))
        t.add(Paragraph("Internal Storage", font_size=Decimal(10)))
        t.add(Paragraph("Sequential Data", font_size=Decimal(10)))
        t.add(Paragraph("Direct Data", font_size=Decimal(10)))
        t.add(Paragraph("Manual Input", font_size=Decimal(10)))

        # third row of shapes
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_manual_operation(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_card(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_paper_tape(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_display(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_preparation(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_loop_limit(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Manual Operation", font_size=Decimal(10)))
        t.add(Paragraph("Card", font_size=Decimal(10)))
        t.add(Paragraph("Paper Tape", font_size=Decimal(10)))
        t.add(Paragraph("Display", font_size=Decimal(10)))
        t.add(Paragraph("Preparation", font_size=Decimal(10)))
        t.add(Paragraph("Loop Limit", font_size=Decimal(10)))

        # fourth row of shapes
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_termination(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_collate(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_delay(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_extract(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_merge(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_or(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Termination", font_size=Decimal(10)))
        t.add(Paragraph("Collate", font_size=Decimal(10)))
        t.add(Paragraph("Delay", font_size=Decimal(10)))
        t.add(Paragraph("Extract", font_size=Decimal(10)))
        t.add(Paragraph("Merge", font_size=Decimal(10)))
        t.add(Paragraph("Or", font_size=Decimal(10)))

        # fifth row of shapes
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_sort(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_summing_junction(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_database(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_on_page_reference(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_off_page_reference(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_process_iso_9000(fixed_bb),
                fill_color=HexColor("f1cd2e"),
                stroke_color=HexColor("000000"),
                line_width=Decimal(1),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # captions
        t.add(Paragraph("Sort", font_size=Decimal(10)))
        t.add(Paragraph("Summing Junction", font_size=Decimal(10)))
        t.add(Paragraph("Database", font_size=Decimal(10)))
        t.add(Paragraph("On Page Reference", font_size=Decimal(10)))
        t.add(Paragraph("Off Page Reference", font_size=Decimal(10)))
        t.add(Paragraph("Process ISO 9000", font_size=Decimal(10)))

        t.set_padding_on_all_cells(Decimal(10), Decimal(10), Decimal(10), Decimal(10))
        layout.add(t)

        # determine output location
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
