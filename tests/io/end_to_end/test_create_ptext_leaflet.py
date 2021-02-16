import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.list import UnorderedList
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Justification,
    Paragraph,
    LineOfText,
)
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../logs/test-create-ptext-leaflet.log", level=logging.DEBUG
)


class TestCreatepTextLeaflet(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../output/test-create-ptext-leaflet")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        layout = MultiColumnLayout(page, number_of_columns=2)

        layout.add(
            LineOfText(
                "pText",
                font_size=Decimal(24),
                font_color=HexColor("8AC926"),
                font="Courier-Bold",
            )
        )
        layout.add(
            LineOfText(
                "The pure Python PDF library",
                font="Helvetica-Oblique",
                font_size=Decimal(8),
                font_color=HexColor("1982C4"),
            )
        )
        layout.add(Paragraph("These are some of the main advantages to using pText:"))
        layout.add(
            UnorderedList()
            .add(Paragraph("100% Python"))
            .add(Paragraph("Tested on a dataset of more than 1000 documents"))
            .add(Paragraph("Type-checked, 100% type-safe"))
            .add(Paragraph("Fully documented"))
        )
        ## 2
        layout.add(
            Paragraph(
                "Think of how effortlessly you could generate invoices, bills, tickets, and much more."
            )
        )
        layout.add(
            Paragraph(
                "With pText, you can easily create the PDF document straight from your code."
            )
        )
        layout.add(
            Paragraph(
                "pText offers several layers of abstraction. You can work with low-level PDF syntax to have precise control over how your content is positioned."
            )
        )
        layout.add(
            Paragraph(
                "But you can also leave the heavy lifting to our PageLayout implementations, which automatically flow content on the page, taking into account margins and other content."
            )
        )
        ### 3
        layout.add(
            Table(number_of_rows=3, number_of_columns=3)
            .add(TableCell(Paragraph(" "), border_top=False, border_left=False))
            .add(
                Paragraph(
                    "When to use Adobe Acrobat", justification=Justification.CENTERED
                )
            )
            .add(Paragraph("When to use pText", justification=Justification.CENTERED))
            .add(Paragraph("Create a single document / template"))
            .add(Paragraph("X", justification=Justification.CENTERED))
            .add(Paragraph(" "))
            .add(Paragraph("Create hundreds of documents, on demand"))
            .add(Paragraph(" "))
            .add(Paragraph("X", justification=Justification.CENTERED))
            .set_border_width_on_all_cells(Decimal(0.2))
        )
        ### 4
        layout.add(
            Paragraph(
                "pText supports all kinds of content you typically see in electronic documents. Text, lists, tables, and combinations thereof. In fact, this entire document was created using pText."
            )
        )
        layout.add(
            Paragraph(
                "pText also supports interactive features, like annotations. Those are the little sticky-notes you might see in a document after someone has added review remarks."
            )
        )
        page.append_text_annotation(
            Rectangle(Decimal(360), Decimal(570), Decimal(32), Decimal(32)),
            contents="Important review remarks here..",
            name_of_icon="Key",
            color=HexColor("1982C4"),
        )
        layout.add(Paragraph(" "))
        layout.add(Paragraph("As well as stamps."))
        page.append_stamp_annotation(
            name="ForPublicRelease",
            rectangle=Rectangle(Decimal(400), Decimal(500), Decimal(100), Decimal(32)),
        )

        layout.add(Paragraph(" "))
        layout.add(
            Paragraph("Actually any graphics can be used for annotations really...")
        )
        page.append_polygon_annotation(
            LineArtFactory.n_pointed_star(
                Rectangle(Decimal(350), Decimal(420), Decimal(32), Decimal(32)), 8
            ),
            stroke_color=HexColor("FF595E"),
        )
        page.append_polygon_annotation(
            LineArtFactory.droplet(
                Rectangle(Decimal(390), Decimal(420), Decimal(32), Decimal(32))
            ),
            stroke_color=HexColor("6A4C93"),
        )
        page.append_polygon_annotation(
            LineArtFactory.sticky_note(
                Rectangle(Decimal(430), Decimal(420), Decimal(32), Decimal(32))
            ),
            stroke_color=HexColor("8AC926"),
        )
        layout.add(Paragraph(" "))
        layout.add(Paragraph(" "))
        layout.add(
            Shape(
                points=LineArtFactory.rectangle(
                    Rectangle(Decimal(0), Decimal(0), Decimal(500), Decimal(2))
                ),
                stroke_color=HexColor("1982C4"),
                fill_color=HexColor("1982C4"),
                line_width=Decimal(1),
                preserve_aspect_ratio=False,
            )
        )
        layout.add(
            Paragraph(
                "Your company isn't boring. Why should your documents be?",
                font_color=HexColor("1982C4"),
                font_size=Decimal(8),
            )
        )
        layout.add(
            Shape(
                points=LineArtFactory.rectangle(
                    Rectangle(Decimal(0), Decimal(0), Decimal(500), Decimal(2))
                ),
                stroke_color=HexColor("1982C4"),
                fill_color=HexColor("1982C4"),
                line_width=Decimal(1),
                preserve_aspect_ratio=False,
            )
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
