import unittest
from datetime import datetime
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.paragraph import Paragraph, Justification
from ptext.pdf.canvas.layout.table import Table, TableCell
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

from PIL import Image as PILImage
import requests


class TestCreateInvoice(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../end_to_end/test-create-invoice")

    def test_write_hello_world(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # logo
        im = PILImage.open(
            requests.get(
                "https://365psd.com/images/listing/fbe/ups-logo-49752.jpg", stream=True
            ).raw
        )
        Image(im).layout(
            page,
            bounding_box=Rectangle(Decimal(20), Decimal(724), Decimal(64), Decimal(64)),
        )

        # Delivery Service Invoice
        Paragraph(
            text="Delivery Service Invoice",
            font_size=Decimal(12),
            font="Helvetica-Oblique",
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(400), Decimal(825), Decimal(160), Decimal(12)
            ),
        )

        # Invoice details table
        t = Table(number_of_rows=5, number_of_columns=2)
        t.add(Paragraph("Invoice Date", font_size=Decimal(8)))
        t.add(
            Paragraph(
                "March 2, 2019",
                font_size=Decimal(8),
                font="Helvetica-Bold",
                font_color=X11Color("Red"),
            )
        )
        t.add(Paragraph("Invoice Number", font_size=Decimal(8)))
        t.add(Paragraph("0003R3Y20099", font_size=Decimal(8)))
        t.add(Paragraph("Shipper Number", font_size=Decimal(8)))
        t.add(Paragraph("secret", font_size=Decimal(8)))
        t.add(Paragraph("Control ID", font_size=Decimal(8)))
        t.add(Paragraph("N844", font_size=Decimal(8)))
        t.add(Paragraph("Page 1 of 4", font_size=Decimal(8)))
        t.add(Paragraph(" "))
        t.no_borders()
        t.layout(
            page,
            bounding_box=Rectangle(
                Decimal(400), Decimal(770), Decimal(160), Decimal(42)
            ),
        )

        # sign up for electronic billing today
        Paragraph(
            "Sign up for electronic billing today! Visit ups.com/billing",
            font="Helvetica-Bold",
            font_size=Decimal(8),
            border_width=Decimal(0.2),
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(400), Decimal(700), Decimal(160), Decimal(50)
            ),
        )

        t = Table(number_of_columns=3, number_of_rows=6)
        t.add(
            TableCell(
                Paragraph("Summary of Charges"),
                col_span=3,
                border_width=Decimal(2),
                border_top=False,
                border_left=False,
                border_right=False,
            )
        )
        t.add(
            TableCell(Paragraph("Page", font_size=Decimal(8)), border_width=Decimal(0))
        )
        t.add(TableCell(Paragraph(" "), border_width=Decimal(0)))
        t.add(
            TableCell(
                Paragraph("Charge", font_size=Decimal(8)), border_width=Decimal(0)
            )
        )
        t.add(TableCell(Paragraph(" ", font_size=Decimal(8)), border_width=Decimal(0)))
        t.add(
            TableCell(
                Paragraph("Outbound", font_size=Decimal(8)), border_width=Decimal(0)
            )
        )
        t.add(TableCell(Paragraph(" ", font_size=Decimal(8)), border_width=Decimal(0)))
        t.add(TableCell(Paragraph("3", font_size=Decimal(8)), border_width=Decimal(0)))
        t.add(
            TableCell(
                Paragraph("Shipping", font_size=Decimal(8)), border_width=Decimal(0)
            )
        )
        t.add(
            TableCell(
                Paragraph("$ 25.20", font_size=Decimal(8)), border_width=Decimal(0)
            )
        )
        t.add(TableCell(Paragraph("3", font_size=Decimal(8)), border_width=Decimal(0)))
        t.add(
            TableCell(
                Paragraph("Adjustments & Other Charges", font_size=Decimal(8)),
                border_width=Decimal(0),
            )
        )
        t.add(
            TableCell(
                Paragraph("$ 46.39", font_size=Decimal(8)), border_width=Decimal(0)
            )
        )
        t.add(
            TableCell(
                Paragraph("Amount due this period", font_size=Decimal(8)),
                col_span=2,
                border_width=Decimal(2),
                border_top=True,
                border_bottom=False,
                border_left=False,
                border_right=False,
            )
        )
        t.add(
            TableCell(
                Paragraph("$ 71.59", font_size=Decimal(8), font_color=X11Color("Red")),
                border_width=Decimal(2),
                border_top=True,
                border_bottom=False,
                border_left=False,
                border_right=False,
            )
        )
        t.layout(
            page,
            bounding_box=Rectangle(
                Decimal(297), Decimal(600), Decimal(297 - 20), Decimal(50)
            ),
        )

        Paragraph(
            text="UPS payment terms require payment of this bill by March 11, 2019",
            font_size=Decimal(9),
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(297), Decimal(500), Decimal(297 - 20), Decimal(50)
            ),
        )
        Paragraph(
            text="Payments received late are subject to a late payment fee of 6% of the Amount Due This Period. \\(see Tarrif/Terms and Conditions of Service at ups.com for details\\)",
            font_size=Decimal(9),
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(297), Decimal(481), Decimal(297 - 20), Decimal(50)
            ),
        )
        Paragraph(
            text="Note: This invoice may contain a fuel surcharge as described atups.com. For more information, please visit ups.com",
            font="Helvetica-Oblique",
            font_size=Decimal(9),
        ).layout(
            page,
            bounding_box=Rectangle(
                Decimal(297), Decimal(481 - 5 * 10), Decimal(297 - 20), Decimal(50)
            ),
        )
        # determine output location
        out_file = self.output_dir / ("output.pdf")

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
