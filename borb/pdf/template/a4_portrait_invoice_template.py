#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class represents an easy way to manipulate a PDF document
that looks like an invoice
"""
import datetime
import io
import re
import string
import time
import typing
from decimal import Decimal
import pathlib

# fmt: off
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.remote_go_to_annotation import RemoteGoToAnnotation
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.page_layout.single_column_layout_with_overflow import SingleColumnLayoutWithOverflow
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.table.table_util import TableUtil
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
# fmt: on


class A4PortraitInvoiceTemplate:
    """
    This class represents an easy way to manipulate a PDF document
    that looks like an invoice
    """

    ACCENT_COLOR: Color = HexColor("#0b3954")
    LIGHT_GRAY_COLOR: Color = HexColor("#eeeeee")

    #
    # CONSTRUCTOR
    #

    def __init__(self):

        # create empty Document
        self._document: Document = Document()

        # create empty Page
        self._page: Page = Page()
        self._document.add_page(self._page)

        # create PageLayout
        self._layout: PageLayout = SingleColumnLayoutWithOverflow(self._page)

        # keep track of the stuff that the user might set
        # we need to keep track because the user might decide to set
        # them in a completely different order than how we'd prefer to display them
        self._address: typing.Optional[typing.Tuple[str, str, str, str, str]] = None
        self._bill_to: typing.Optional[typing.Tuple[str, str, str, str, str]] = None
        self._company_logo: typing.Optional[typing.Union[str, pathlib.Path]] = None
        self._currency_abbreviation: typing.Optional[str] = None
        self._creation_date_in_ms: typing.Optional[int] = None
        self._ship_to: typing.Optional[typing.Tuple[str, str, str, str, str]] = None
        self._due_date_in_ms: typing.Optional[int] = None
        self._items: typing.List[typing.Tuple[str, str, float, float, float]] = []
        self._notes: typing.Optional[str] = None
        self._nr: typing.Optional[str] = None
        self._subtotal: typing.Optional[float] = None
        self._terms: typing.Optional[str] = None
        self._total: typing.Optional[float] = None
        self._vat: typing.Optional[float] = None

    #
    # PRIVATE
    #

    def _add_page_numbers(self) -> None:
        N: int = int(
            self._document.get_document_info().get_number_of_pages() or Decimal(0)
        )
        for i in range(0, N):
            s: Page = self._document.get_page(i)
            # add blue square
            ConnectedShape(
                LineArtFactory.rectangle(
                    Rectangle(Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47))
                ),
                stroke_color=A4PortraitInvoiceTemplate.ACCENT_COLOR,
                fill_color=A4PortraitInvoiceTemplate.ACCENT_COLOR,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )
            # add Paragraph
            Paragraph(
                f"{i+1}",
                font_size=Decimal(10),
                font_color=A4PortraitInvoiceTemplate.LIGHT_GRAY_COLOR,
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )

    def _add_paragraph_with_hyperlinks(
        self, text: str, page_layout: PageLayout
    ) -> None:
        URL_REGEX = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

        # IF there are no urls
        # THEN return a regular old Paragraph
        W: Decimal = page_layout.get_page().get_page_info().get_width() or Decimal(0)
        if len(re.findall(URL_REGEX, text)) == 0:
            page_layout.add(Paragraph(text, padding_left=W * Decimal(0.05)))
            return

        # tokenize the text
        chunks_of_text: typing.List[typing.Tuple[ChunkOfText, str, bool]] = [
            (ChunkOfText(x + " "), x, re.match(URL_REGEX, x) is not None)
            for x in text.split(" ")
        ]

        # modify tokens we have overlooked because they end
        # with a punctuation mark, rather than a space
        i: int = 0
        while i < len(chunks_of_text):
            txt: str = chunks_of_text[i][1]
            if (
                txt[-1] in string.punctuation
                and re.match(URL_REGEX, txt[:-1]) is not None
            ):
                chunks_of_text.pop(i)
                chunks_of_text.insert(i, (ChunkOfText(txt[:-1]), txt[:-1], True))
                chunks_of_text.insert(
                    i + 1, (ChunkOfText(txt[-1] + " "), txt[-1] + " ", False)
                )
                i += 2
                continue
            i += 1

        # change the font_color where needed
        for chunk_of_text, url, should_be_marked in chunks_of_text:
            if not should_be_marked:
                continue
            chunk_of_text._font_color = HexColor("0b3954")
            chunk_of_text._font = StandardType1Font("Helvetica-Bold")

        # build and add HeterogeneousParagraph
        page_layout.add(
            HeterogeneousParagraph(
                [t[0] for t in chunks_of_text], padding_left=W * Decimal(0.05)
            )
        )

        # add RemoteGoToAnnotation where needed
        for chunk_of_text, url, should_be_marked in chunks_of_text:
            if not should_be_marked:
                continue
            previous_layout_box: typing.Optional[
                Rectangle
            ] = chunk_of_text.get_previous_layout_box()
            assert previous_layout_box is not None
            page_layout.get_page().add_annotation(
                RemoteGoToAnnotation(previous_layout_box, url)
            )

    def _build(self) -> None:

        # Fill in all defaults
        # _address
        if self._address is None:
            self._address = (
                "<address line 1>",
                "<address line 2>",
                "<address line 3>",
                "<company name>",
                "<first name> <last name>",
            )

        # _bill_to
        if self._bill_to is None and self._ship_to is not None:
            self._bill_to = self._ship_to

        # _creation_date_in_ms
        if self._creation_date_in_ms is None:
            self._creation_date_in_ms = int(time.time() * 1000)

        # _currency_abbreviation
        if self._currency_abbreviation is None:
            self._currency_abbreviation = "USD"

        # _deliver_to
        if self._ship_to is None and self._bill_to is not None:
            self._ship_to = self._bill_to

        # _due_date_in_ms
        if self._due_date_in_ms is None:
            self._due_date_in_ms = self._creation_date_in_ms + (2 * 7 * 86400000)

        # _nr
        if self._nr is None:
            self._nr = datetime.datetime.now().strftime("%Y%m%d001")

        # _subtotal
        if self._subtotal is None:
            self._subtotal = sum([x[4] for x in self._items])
        assert self._subtotal is not None

        # _total
        if self._total is None:
            if self._vat is None:
                self._vat = self._subtotal * 0.10
            self._total = self._subtotal + self._vat
        assert self._total is not None

        # _vat
        if self._vat is None:
            self._vat = self._subtotal * 0.10
        assert self._vat is not None

        # add logo to PageLayout
        THIRTY_TWO: Decimal = Decimal(32)
        if self._company_logo is not None:
            Image(
                self._company_logo,
                width=THIRTY_TWO,
                height=THIRTY_TWO,
                padding_top=THIRTY_TWO,
                padding_left=THIRTY_TWO,
            ).paint(
                self._layout.get_page(),
                Rectangle(
                    Decimal(0),
                    842 - THIRTY_TWO * Decimal(2),
                    THIRTY_TWO * Decimal(2),
                    THIRTY_TWO * Decimal(2),
                ),
            )

        # add (our) address and invoice information
        date_as_str: str = time.strftime(
            "%d-%m-%Y", time.gmtime(self._creation_date_in_ms / 1000)
        )
        due_date_as_str: str = time.strftime(
            "%d-%m-%Y", time.gmtime(self._due_date_in_ms / 1000)
        )
        self._layout.add(
            FixedColumnWidthTable(
                number_of_columns=3,
                number_of_rows=5,
                column_widths=[Decimal(50), Decimal(25), Decimal(25)],
            )
            # row 1
            .add(Paragraph(f"{self._address[0]}"))
            .add(
                Paragraph(
                    "Date", font="Helvetica-bold", horizontal_alignment=Alignment.RIGHT
                )
            )
            .add(Paragraph(f"{date_as_str}"))
            # row 2
            .add(Paragraph(f"{self._address[1]}"))
            .add(
                Paragraph(
                    "Invoice#",
                    font="Helvetica-bold",
                    horizontal_alignment=Alignment.RIGHT,
                )
            )
            .add(Paragraph(f"{self._nr}"))
            # row 3
            .add(Paragraph(f"{self._address[2]}"))
            .add(
                Paragraph(
                    "Due Date",
                    font="Helvetica-bold",
                    horizontal_alignment=Alignment.RIGHT,
                )
            )
            .add(Paragraph(f"{due_date_as_str}"))
            # row 4
            .add(Paragraph(f"{self._address[3]}"))
            .add(Paragraph(""))
            .add(Paragraph(""))
            # row 5
            .add(Paragraph(f"{self._address[4]}"))
            .add(Paragraph(""))
            .add(Paragraph(""))
            .set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
            .no_borders()
        )

        # add _bill_to and _ship_to
        if self._bill_to is not None and self._ship_to is not None:
            self._layout.add(Paragraph(""))
            self._layout.add(
                TableUtil.from_2d_array(
                    [
                        ["BILL TO", "SHIP TO"],
                        [self._bill_to[0], self._ship_to[0]],
                        [self._bill_to[1], self._ship_to[1]],
                        [self._bill_to[2], self._ship_to[2]],
                        [self._bill_to[3], self._ship_to[3]],
                        [self._bill_to[4], self._ship_to[4]],
                    ],
                    flexible_column_width=False,
                ).no_borders()
            )

        # add itemized table
        self._layout.add(Paragraph(""))
        itemized_table: Table = FixedColumnWidthTable(
            number_of_columns=4, number_of_rows=5 + len(self._items)
        )

        # row 1
        itemized_table.add(
            TableCell(
                Paragraph("DESCRIPTION", font="Helvetica-bold"),
                background_color=HexColor("f1f3f4"),
            )
        )
        itemized_table.add(
            TableCell(
                Paragraph("QTY", font="Helvetica-bold"),
                background_color=HexColor("f1f3f4"),
            )
        )
        itemized_table.add(
            TableCell(
                Paragraph("UNIT PRICE", font="Helvetica-bold"),
                background_color=HexColor("f1f3f4"),
            )
        )
        itemized_table.add(
            TableCell(
                Paragraph("AMOUNT", font="Helvetica-bold"),
                background_color=HexColor("f1f3f4"),
            )
        )

        # row 2
        for item in self._items:
            itemized_table.add(Paragraph(f"{item[1]}"))
            itemized_table.add(Paragraph(f"{item[2]}"))
            itemized_table.add(Paragraph(f"{item[3]}"))
            itemized_table.add(Paragraph(f"{item[4]}"))

        # row 3
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph(""))

        # row 4
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph("Subtotal", font="Helvetica-bold"))
        itemized_table.add(
            Paragraph(
                f"{self._subtotal} {self._currency_abbreviation}", font="Helvetica-bold"
            )
        )

        # row 5
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph("VAT", font="Helvetica-bold"))
        itemized_table.add(
            Paragraph(
                f"{self._vat} {self._currency_abbreviation}", font="Helvetica-bold"
            )
        )

        # row 6
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph(""))
        itemized_table.add(Paragraph("Total", font="Helvetica-bold"))
        itemized_table.add(
            Paragraph(
                f"{self._total} {self._currency_abbreviation}", font="Helvetica-bold"
            )
        )

        itemized_table.set_padding_on_all_cells(
            Decimal(3), Decimal(3), Decimal(3), Decimal(3)
        )
        itemized_table.no_borders()
        self._layout.add(itemized_table)

        # spacing
        if self._terms is not None or self._notes is not None:
            self._layout.add(Paragraph(""))

        # add _terms
        if self._terms is not None:
            self._layout.add(
                Paragraph(
                    "TERMS",
                    font="Helvetica-Bold",
                )
            )
            self._add_paragraph_with_hyperlinks(self._terms, self._layout)

        # add _notes
        if self._notes is not None:
            self._layout.add(
                Paragraph(
                    "NOTES",
                    font="Helvetica-Bold",
                )
            )
            self._add_paragraph_with_hyperlinks(self._notes, self._layout)

    #
    # PUBLIC
    #

    def add_item(
        self,
        description: str,
        name: str,
        quantity: int,
        unit_price: float,
        total_price: typing.Optional[float] = None,
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function adds an item to this A4PortraitInvoiceTemplate
        :param description:     the description of the item to be added
        :param name:            the name of the item to be added
        :param quantity:        the quantity(ies) of the item(s) to be added
        :param unit_price:      the unit price of the item to be added
        :param total_price:     the total price of the item(s) to be added
        :return:                self
        """
        self._items.append(
            (
                description,
                name,
                quantity,
                unit_price,
                total_price or (unit_price * quantity),
            )
        )
        return self

    def bytes(self) -> bytes:
        """
        This function returns the bytes representing this A4PortraitInvoiceTemplate.
        It does so by saving this A4PortraitInvoiceTemplate to an io.BytesIO buffer,
        and returning its bytes.
        :return:    the bytes representing this A4PortraitInvoiceTemplate
        """
        self._build()
        self._add_page_numbers()
        buffer = io.BytesIO()
        PDF.dumps(buffer, self._document)
        buffer.seek(0)
        return buffer.getvalue()

    def save(
        self, path_or_str: typing.Union[str, pathlib.Path]
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function stores this InvoiceTemplate at the given path
        :param path_or_str:     the path or str representing the location at which to store this A4PortraitInvoiceTemplate
        :return:                self
        """
        self._build()
        self._add_page_numbers()
        with open(path_or_str, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self._document)
        return self

    def set_address(
        self,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        company_name: str,
        name: str,
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the address to be used as YOUR company address for this A4PortraitInvoiceTemplate
        :param address_line_1:  address line 1
        :param address_line_2:  address line 2
        :param address_line_3:  address line 3
        :param company_name:    the company name
        :param name:            the name of the person
        :return:                self
        """
        self._address = (
            address_line_1,
            address_line_2,
            address_line_3,
            company_name,
            name,
        )
        return self

    def set_bill_to(
        self,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        company_name: str,
        name: str,
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the address to be used as the BILL TO company address for this A4PortraitInvoiceTemplate
        :param address_line_1:  address line 1
        :param address_line_2:  address line 2
        :param address_line_3:  address line 3
        :param company_name:    the company name
        :param name:            the name of the person
        :return:                self
        """
        self._bill_to = (
            address_line_1,
            address_line_2,
            address_line_3,
            company_name,
            name,
        )
        return self

    def set_company_logo(
        self, path_or_uri: typing.Union[str, pathlib.Path]
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the URI (str) or Path for the company logo
        :param path_or_uri:     the URI (str) or Path
        :return:                self
        """
        self._company_logo = path_or_uri
        return self

    def set_creation_date(self, date_in_ms: int) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the creation date of this A4PortraitInvoiceTemplate.
        The default is today.
        :param date_in_ms:  the creation date of this A4PortraitInvoiceTemplate
        :return:            self
        """
        self._creation_date_in_ms = date_in_ms
        return self

    def set_currency_abbreviation(
        self, abbreviation: str
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the abbreviation for the currency used on this A4PortraitInvoiceTemplate.
        The default is "USD"
        :param abbreviation:    the currency abbreviation
        :return:                self
        """
        self._currency_abbreviation = abbreviation
        return self

    def set_due_date(self, date_in_ms: int) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the due date of this A4PortraitInvoiceTemplate.
        The default is the creation date + 14 days.
        :param date_in_ms:  the due date of this A4PortraitInvoiceTemplate
        :return:            self
        """
        self._due_date_in_ms = date_in_ms
        return self

    def set_notes(self, notes: str) -> "A4PortraitInvoiceTemplate":
        """
        This function adds a "notes" section to this A4PortraitInvoiceTemplate
        :param notes:   the note(s) to be added
        :return:        self
        """
        self._notes = notes
        return self

    def set_nr(self, nr: str) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the (invoice) nr of this A4PortraitInvoiceTemplate.
        The default is {year}{month}{day}001
        :param nr:  the (invoice) nr
        :return:    self
        """
        self._nr = nr
        return self

    def set_ship_to(
        self,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        company_name: str,
        name: str,
    ) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the address to be used as the SHIP TO company address for this A4PortraitInvoiceTemplate
        :param address_line_1:  address line 1
        :param address_line_2:  address line 2
        :param address_line_3:  address line 3
        :param company_name:    the company name
        :param name:            the name of the person
        :return:                self
        """
        self._ship_to = (
            address_line_1,
            address_line_2,
            address_line_3,
            company_name,
            name,
        )
        return self

    def set_subtotal(self, amount: float) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the subtotal for this A4PortraitInvoiceTemplate.
        The default is the sum of all items on this A4PortraitInvoiceTemplate.
        :param amount:      the subtotal
        :return:            self
        """
        self._subtotal = amount
        return self

    def set_terms(self, terms: str) -> "A4PortraitInvoiceTemplate":
        """
        This function adds a "terms" section to this A4PortraitInvoiceTemplate
        :param notes:   the term(s) to be added
        :return:        self
        """
        self._terms = terms
        return self

    def set_total(self, amount: float) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the total for this A4PortraitInvoiceTemplate.
        The default is the sum of all items on this A4PortraitInvoiceTemplate + the VAT.
        :param amount:      the total
        :return:            self
        """
        self._total = amount
        return self

    def set_vat(self, amount: float) -> "A4PortraitInvoiceTemplate":
        """
        This function sets the VAT for this A4PortraitInvoiceTemplate.
        The default is 10% of the sum of all items on this A4PortraitInvoiceTemplate.
        :param amount:      the VAT
        :return:            self
        """
        self._vat = amount
        return self
