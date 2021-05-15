import json
import logging
import random
import unittest
from datetime import datetime
from pathlib import Path

from ptext.pdf.canvas.layout.layout_element import LayoutElement

from ptext.pdf.canvas.layout.table import Table, TableCell

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor, X11Color, Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import (
    MultiColumnLayout,
    SingleColumnLayout,
    PageLayout,
)
from ptext.pdf.canvas.layout.paragraph import (
    Alignment,
    Paragraph,
)
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page, DestinationType
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-realistic-invoice.log"),
    level=logging.DEBUG,
)


class TestWriteRealisticInvoice(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-realistic-invoice")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
        page_layout.add(
            Image(
                "https://www.designevo.com/res/templates/thumb_small/green-and-white-stripe-sphere.png",
                width=Decimal(128),
                height=Decimal(128),
            )
        )

        # invoice information table
        page_layout.add(self._build_invoice_information())

        # empty paragraph for spacing
        page_layout.add(Paragraph(" "))

        # billing and shipping information
        page_layout.add(self._build_billing_and_shipping_information())

        # empty paragraph for spacing
        page_layout.add(Paragraph(" "))

        # itemized description
        page_layout.add(self._build_itemized_description_table())

        # outline
        pdf.add_outline("Your Invoice", 0, DestinationType.FIT, page_nr=0)

        # embed json document for machine processing
        invoice_json = {
            "items": [
                {
                    "Description": "Product1",
                    "Quantity": 2,
                    "Unit Price": 50,
                    "Amount": 100,
                },
                {
                    "Description": "Product2",
                    "Quantity": 4,
                    "Unit Price": 60,
                    "Amount": 100,
                },
                {
                    "Description": "Labor",
                    "Quantity": 14,
                    "Unit Price": 60,
                    "Amount": 100,
                },
            ],
            "Subtotal": 1180,
            "Discounts": 177,
            "Taxes": 100.30,
            "Total": 1163.30,
        }
        invoice_json_bytes = bytes(
            json.dumps(invoice_json, indent=4), encoding="latin1"
        )
        pdf.append_embedded_file(
            "invoice.json", invoice_json_bytes, apply_compression=False
        )

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

    def _build_invoice_information(self) -> LayoutElement:
        table_001: Table = Table(number_of_rows=5, number_of_columns=3)
        table_001.add(Paragraph("[Street Address]"))
        table_001.add(
            Paragraph(
                "Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            )
        )
        now = datetime.now()
        table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
        table_001.add(Paragraph("[City, State, ZIP Code]"))
        table_001.add(
            Paragraph(
                "Invoice #", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            )
        )
        table_001.add(Paragraph("%d" % random.randint(1000, 10000)))
        table_001.add(Paragraph("[Phone]"))
        table_001.add(
            Paragraph(
                "Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            )
        )
        table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
        table_001.add(Paragraph("[Email Address]"))
        table_001.add(Paragraph(" "))
        table_001.add(Paragraph(" "))
        table_001.add(Paragraph("[Company Website]"))
        table_001.add(Paragraph(" "))
        table_001.add(Paragraph(" "))
        table_001.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        table_001.no_borders()
        return table_001

    def _build_billing_and_shipping_information(self) -> LayoutElement:
        table_001: Table = Table(number_of_rows=6, number_of_columns=2)
        table_001.add(
            Paragraph(
                "BILL TO",
                background_color=HexColor("016934"),
                font_color=X11Color("White"),
            )
        )
        table_001.add(
            Paragraph(
                "SHIP TO",
                background_color=HexColor("016934"),
                font_color=X11Color("White"),
            )
        )
        table_001.add(Paragraph("[Recipient Name]"))  # BILLING
        table_001.add(Paragraph("[Recipient Name]"))  # SHIPPING
        table_001.add(Paragraph("[Company Name]"))  # BILLING
        table_001.add(Paragraph("[Company Name]"))  # SHIPPING
        table_001.add(Paragraph("[Street Address]"))  # BILLING
        table_001.add(Paragraph("[Street Address]"))  # SHIPPING
        table_001.add(Paragraph("[City, State, ZIP Code]"))  # BILLING
        table_001.add(Paragraph("[City, State, ZIP Code]"))  # SHIPPING
        table_001.add(Paragraph("[Phone]"))  # BILLING
        table_001.add(Paragraph("[Phone]"))  # SHIPPING
        table_001.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        table_001.no_borders()
        return table_001

    def _build_itemized_description_table(self) -> LayoutElement:
        table_001: Table = Table(number_of_rows=15, number_of_columns=4)
        for h in ["DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT"]:
            table_001.add(
                TableCell(
                    Paragraph(h, font_color=X11Color("White")),
                    background_color=HexColor("016934"),
                )
            )

        odd_color: Color = HexColor("BBBBBB")
        even_color: Color = HexColor("FFFFFF")
        for row_number, item in enumerate(
            [("Product 1", 2, 50), ("Product 2", 4, 60), ("Labor", 14, 60)]
        ):
            c = even_color if row_number % 2 == 0 else odd_color
            table_001.add(TableCell(Paragraph(item[0]), background_color=c))
            table_001.add(TableCell(Paragraph(str(item[1])), background_color=c))
            table_001.add(TableCell(Paragraph("$ " + str(item[2])), background_color=c))
            table_001.add(
                TableCell(Paragraph("$ " + str(item[1] * item[2])), background_color=c)
            )

        for row_number in range(3, 10):
            c = even_color if row_number % 2 == 0 else odd_color
            for _ in range(0, 4):
                table_001.add(TableCell(Paragraph(" "), background_color=c))

        table_001.add(
            TableCell(
                Paragraph(
                    "Subtotal",
                    font="Helvetica-Bold",
                    horizontal_alignment=Alignment.RIGHT,
                ),
                col_span=3,
            )
        )
        table_001.add(
            TableCell(Paragraph("$ 1,180.00", horizontal_alignment=Alignment.RIGHT))
        )
        table_001.add(
            TableCell(
                Paragraph(
                    "Discounts",
                    font="Helvetica-Bold",
                    horizontal_alignment=Alignment.RIGHT,
                ),
                col_span=3,
            )
        )
        table_001.add(
            TableCell(Paragraph("$ 177.00", horizontal_alignment=Alignment.RIGHT))
        )
        table_001.add(
            TableCell(
                Paragraph(
                    "Taxes", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
                ),
                col_span=3,
            )
        )
        table_001.add(
            TableCell(Paragraph("$ 100.30", horizontal_alignment=Alignment.RIGHT))
        )
        table_001.add(
            TableCell(
                Paragraph(
                    "Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
                ),
                col_span=3,
            )
        )
        table_001.add(
            TableCell(Paragraph("$ 1163.30", horizontal_alignment=Alignment.RIGHT))
        )
        table_001.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        table_001.no_borders()
        return table_001
