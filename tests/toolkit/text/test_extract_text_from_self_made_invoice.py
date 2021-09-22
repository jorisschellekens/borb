import datetime
import random
import unittest
from decimal import Decimal

import typing
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table, TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.location.location_filter import LocationFilter
from borb.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
    PDFMatch,
)
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractTextFromSelfMadeInvoice(unittest.TestCase):
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

    def _build_invoice_information(self) -> Table:
        """
        This function builds a Table containing invoice information
        :return:    a Table containing invoice information
        """
        table_001 = FixedColumnWidthTable(number_of_rows=5, number_of_columns=3)

        table_001.add(Paragraph("[Street Address]"))
        table_001.add(
            Paragraph(
                "Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            )
        )
        now = datetime.datetime.now()
        table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))

        # fmt: off
        table_001.add(Paragraph("[City, State, ZIP Code]"))
        table_001.add(Paragraph("Invoice #", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        table_001.add(Paragraph("%d" % random.randint(1000, 10000)))
        # fmt: on

        # fmt: off
        table_001.add(Paragraph("[Phone]"))
        table_001.add(Paragraph("Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
        # fmt: on

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

    def _build_billing_and_shipping_information(self) -> Table:
        """
        This function builds a Table containing billing and shipping information
        :return:    a Table containing shipping and billing information
        """
        table_001 = FixedColumnWidthTable(number_of_rows=6, number_of_columns=2)
        table_001.add(
            Paragraph(
                "BILL TO",
                background_color=HexColor("263238"),
                font_color=X11Color("White"),
            )
        )
        table_001.add(
            Paragraph(
                "SHIP TO",
                background_color=HexColor("263238"),
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

    class Product:
        """
        This class represents a purchased product
        """

        def __init__(self, name: str, quantity: int, price_per_sku: float):
            self.name: str = name
            assert quantity >= 0
            self.quantity: int = quantity
            assert price_per_sku >= 0
            self.price_per_sku: float = price_per_sku

    def _build_itemized_description_table(self, products: typing.List[Product] = []):
        """
        This function builds a Table containing itemized billing information
        :param:     products
        :return:    a Table containing itemized billing information
        """
        table_001 = FixedColumnWidthTable(number_of_rows=15, number_of_columns=4)
        for h in ["DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT"]:
            table_001.add(
                TableCell(
                    Paragraph(h, font_color=X11Color("White")),
                    background_color=HexColor("0b3954"),
                )
            )

        odd_color = HexColor("BBBBBB")
        even_color = HexColor("FFFFFF")
        for row_number, item in enumerate(products):
            c = even_color if row_number % 2 == 0 else odd_color
            table_001.add(TableCell(Paragraph(item.name), background_color=c))
            table_001.add(TableCell(Paragraph(str(item.quantity)), background_color=c))
            table_001.add(
                TableCell(Paragraph("$ " + str(item.price_per_sku)), background_color=c)
            )
            table_001.add(
                TableCell(
                    Paragraph("$ " + str(item.quantity * item.price_per_sku)),
                    background_color=c,
                )
            )

        # Optionally add some empty rows to have a fixed number of rows for styling purposes
        for row_number in range(len(products), 10):
            c = even_color if row_number % 2 == 0 else odd_color
            for _ in range(0, 4):
                table_001.add(TableCell(Paragraph(" "), background_color=c))

        # subtotal
        subtotal: float = sum([x.price_per_sku * x.quantity for x in products])
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

        # discounts
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
            TableCell(Paragraph("$ 0.00", horizontal_alignment=Alignment.RIGHT))
        )

        # taxes
        taxes: float = subtotal * 0.06
        table_001.add(
            TableCell(
                Paragraph(
                    "Taxes", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
                ),
                col_span=3,
            )
        )
        table_001.add(
            TableCell(
                Paragraph("$ " + str(taxes), horizontal_alignment=Alignment.RIGHT)
            )
        )

        # total
        total: float = subtotal + taxes
        table_001.add(
            TableCell(
                Paragraph(
                    "Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
                ),
                col_span=3,
            )
        )
        table_001.add(
            TableCell(
                Paragraph("$ " + str(total), horizontal_alignment=Alignment.RIGHT)
            )
        )
        table_001.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        table_001.no_borders()
        return table_001

    def test_generate_invoice(self):

        # create Document
        doc: Document = Document()

        # add Page
        page: Page = Page()
        doc.append_page(page)

        # set PageLayout
        page_layout: PageLayout = SingleColumnLayout(
            page, vertical_margin=page.get_page_info().get_height() * Decimal(0.02)
        )

        # add corporate logo
        page_layout.add(
            Image(
                "https://github.com/jorisschellekens/borb/blob/master/logo/borb_64.png?raw=true",
                width=Decimal(64),
                height=Decimal(64),
            )
        )

        # Invoice information table
        page_layout.add(self._build_invoice_information())

        # Empty paragraph for spacing
        page_layout.add(Paragraph(" "))

        # Billing and shipping information table
        page_layout.add(self._build_billing_and_shipping_information())

        # Empty paragraph for spacing
        page_layout.add(Paragraph(" "))

        # Itemized description
        page_layout.add(
            self._build_itemized_description_table(
                [
                    TestExtractTextFromSelfMadeInvoice.Product("Product 1", 2, 50),
                    TestExtractTextFromSelfMadeInvoice.Product("Product 2", 4, 60),
                    TestExtractTextFromSelfMadeInvoice.Product("Labor", 14, 60),
                ]
            )
        )

        # store
        with open(self.output_dir / "output.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_extract_text(self):

        r: Rectangle = Rectangle(Decimal(280), Decimal(500), Decimal(200), Decimal(130))
        l0: LocationFilter = LocationFilter(r)
        l1: SimpleTextExtraction = SimpleTextExtraction()
        l0.add_listener(l1)

        d: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as pdf_file_handle:
            d = PDF.loads(pdf_file_handle, [l0])

        # check whether document could be read without issues
        assert d is not None

        # check text
        assert (
            l1.get_text_for_page(0)
            == "SHIP TO\n[Recipient Name]\n[Company Name]\n[Street Address]\n[City, State, ZIP Code]\n[Phone]"
        )

    def test_match_regular_expression(self):

        l: RegularExpressionTextExtraction = RegularExpressionTextExtraction("SHIP TO")
        d: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as pdf_file_handle:
            d = PDF.loads(pdf_file_handle, [l])

        # check whether document could be read without issues
        assert d is not None

        matches: typing.List[PDFMatch] = l.get_matches_for_page(0)
        assert len(matches) == 1

        r: Rectangle = matches[0].get_bounding_boxes()[0]

        assert 298 <= r.get_x() <= 301
        assert 594 <= r.get_y() <= 596

    def test_match_regular_expression_use_location(self):

        #
        # 1. MATCH REGULAR EXPRESSION
        #

        l0: RegularExpressionTextExtraction = RegularExpressionTextExtraction("SHIP TO")
        d: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as pdf_file_handle:
            d = PDF.loads(pdf_file_handle, [l0])

        matches: typing.List[PDFMatch] = l0.get_matches_for_page(0)
        assert len(matches) == 1

        ship_to_rectangle: Rectangle = matches[0].get_bounding_boxes()[0]

        #
        # 2. EXTRACT TEXT USING RECTANGLE
        #

        r: Rectangle = Rectangle(
            ship_to_rectangle.get_x() - Decimal(50),
            ship_to_rectangle.get_y() - Decimal(100),
            Decimal(200),
            Decimal(130),
        )

        # set up EventListener(s)
        l1: LocationFilter = LocationFilter(r)
        l2: SimpleTextExtraction = SimpleTextExtraction()
        l1.add_listener(l2)

        with open(self.output_dir / "output.pdf", "rb") as pdf_file_handle:
            d = PDF.loads(pdf_file_handle, [l1])

        print(l2.get_text_for_page(0))
