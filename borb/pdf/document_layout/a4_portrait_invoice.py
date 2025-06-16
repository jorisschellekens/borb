#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represent an invoice in A4 portrait format.

The `A4PortraitInvoice` class enables users to create and customize an invoice in A4 portrait layout.
It provides methods to set various invoice properties, including the company's address, billing and
shipping addresses, line items, taxes, discounts, and payment terms.
"""
import datetime
import pathlib
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.document_layout.document_layout import DocumentLayout
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.visitor.pdf import PDF


class A4PortraitInvoice(DocumentLayout):
    """
    Represent an invoice in A4 portrait format.

    The `A4PortraitInvoice` class enables users to create and customize an invoice in A4 portrait layout.
    It provides methods to set various invoice properties, including the company's address, billing and
    shipping addresses, line items, taxes, discounts, and payment terms.
    """

    __LIGHT_GRAY: Color = X11Color.LIGHT_GRAY

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a new instance of the A4PortraitInvoice class.

        This constructor sets up the initial state of the invoice object, initializing attributes that will
        hold the various components of the invoice, including company and customer information, line items,
        tax and discount values, and other relevant details.
        """
        super().__init__()
        self.__address_lines: typing.List[str] = []  # type: ignore[annotation-unchecked]
        self.__bill_to_address_lines: typing.Optional[typing.List[str]] = None  # type: ignore[annotation-unchecked]
        self.__currency_abbreviation: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__date: typing.Optional[datetime.datetime] = None  # type: ignore[annotation-unchecked]
        self.__discounts: typing.Optional[float] = None  # type: ignore[annotation-unchecked]
        self.__document: typing.Optional[Document] = None  # type: ignore[annotation-unchecked]
        self.__due_date: typing.Optional[datetime.datetime] = None  # type: ignore[annotation-unchecked]
        self.__items: typing.List[typing.Tuple[float, str, int, float]] = []  # type: ignore[annotation-unchecked]
        self.__logo: typing.Optional[  # type: ignore[annotation-unchecked]
            typing.Union[bytes, pathlib.Path, "PIL.Image.Image", str]
        ] = None
        self.__invoice_nr: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__ship_to_address_lines: typing.Optional[typing.List[str]] = None  # type: ignore[annotation-unchecked]
        self.__subtotal: typing.Optional[float] = None  # type: ignore[annotation-unchecked]
        self.__taxes: typing.Optional[float] = None  # type: ignore[annotation-unchecked]
        self.__terms_and_conditions: typing.Optional[str] = None  # type: ignore[annotation-unchecked]
        self.__total: typing.Optional[float] = None  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    def __build(self) -> None:
        # set __bill_to_address_lines
        if self.__bill_to_address_lines is None:
            self.__bill_to_address_lines = ["" for _ in range(0, 5)]

        # set __currency_abbreviation
        if self.__currency_abbreviation is None:
            self.__currency_abbreviation = "USD"

        # set __date
        now: datetime.datetime = datetime.datetime.now()
        if self.__date is None:
            self.__date = now

        # set __discounts
        if self.__discounts is None:
            self.__discounts = 0

        # set __due_date
        if self.__due_date is None:
            self.__due_date = self.__date + datetime.timedelta(days=7)

        # set __invoice_nr
        if self.__invoice_nr is None:
            self.__invoice_nr = f"{now.year}{now.month:02}{now.day:02}001"

        # set __ship_to_address_lines
        if self.__ship_to_address_lines is None:
            self.__ship_to_address_lines = ["" for _ in range(0, 5)]

        # set __subtotal
        if self.__subtotal is None:
            self.__subtotal = sum([x[0] for x in self.__items] + [0])

        # set __taxes
        if self.__taxes is None:
            self.__taxes = round(
                (sum([x[0] for x in self.__items] + [0]) - self.__discounts) * 0.06, 2
            )

        # set __terms_and_conditions
        if self.__terms_and_conditions is None:
            self.__terms_and_conditions = ""

        # set __total
        if self.__total is None:
            self.__total = self.__subtotal - self.__discounts + self.__taxes

        # start building the PDF
        self.__document = Document()

        page: Page = Page()
        self.__document.append_page(page)

        # add logo
        layout: PageLayout = SingleColumnLayout(page)
        layout.append_layout_element(
            Image(
                bytes_path_pil_image_or_url=self.__logo,
                size=(64, 64),
                horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
                vertical_alignment=LayoutElement.VerticalAlignment.TOP,
            )
        )

        # add address, date, due date, invoice nr
        layout.append_layout_element(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=5)
            .append_layout_element(Chunk(self.__address_lines[0]))
            .append_layout_element(
                HeterogeneousParagraph(
                    [
                        Chunk("Date: ", font=Standard14Fonts.get("Helvetica-Bold")),
                        Chunk(
                            f"{self.__date.day:02}-{self.__date.month:02}-{self.__date.year}"
                        ),
                    ]
                )
            )
            .append_layout_element(Chunk(self.__address_lines[1]))
            .append_layout_element(
                HeterogeneousParagraph(
                    [
                        Chunk("Due Date: ", font=Standard14Fonts.get("Helvetica-Bold")),
                        Chunk(
                            f"{self.__due_date.day:02}-{self.__due_date.month:02}-{self.__due_date.year}"
                        ),
                    ]
                )
            )
            .append_layout_element(Chunk(self.__address_lines[2]))
            .append_layout_element(
                HeterogeneousParagraph(
                    [
                        Chunk(
                            "Invoice Nr: ", font=Standard14Fonts.get("Helvetica-Bold")
                        ),
                        Chunk(f"{self.__invoice_nr}"),
                    ]
                )
            )
            .append_layout_element(Chunk(self.__address_lines[3]))
            .append_layout_element(Chunk(" "))
            .append_layout_element(Chunk(self.__address_lines[4]))
            .append_layout_element(Chunk(" "))
            .set_padding_on_all_cells(
                padding_top=2, padding_right=2, padding_bottom=2, padding_left=2
            )
            .no_borders()
        )

        # add ship to, bill to
        layout.append_layout_element(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=6)
            .append_layout_element(
                Table.TableCell(
                    Chunk("BILL TO", font=Standard14Fonts.get("Helvetica-Bold")),
                    background_color=A4PortraitInvoice.__LIGHT_GRAY,
                )
            )
            .append_layout_element(
                Table.TableCell(
                    Chunk("SHIP TO", font=Standard14Fonts.get("Helvetica-Bold")),
                    background_color=A4PortraitInvoice.__LIGHT_GRAY,
                )
            )
            .append_layout_element(Chunk(self.__bill_to_address_lines[0]))
            .append_layout_element(Chunk(self.__ship_to_address_lines[0]))
            .append_layout_element(Chunk(self.__bill_to_address_lines[1]))
            .append_layout_element(Chunk(self.__ship_to_address_lines[1]))
            .append_layout_element(Chunk(self.__bill_to_address_lines[2]))
            .append_layout_element(Chunk(self.__ship_to_address_lines[2]))
            .append_layout_element(Chunk(self.__bill_to_address_lines[3]))
            .append_layout_element(Chunk(self.__ship_to_address_lines[3]))
            .append_layout_element(Chunk(self.__bill_to_address_lines[4]))
            .append_layout_element(Chunk(self.__ship_to_address_lines[4]))
            .set_padding_on_all_cells(
                padding_top=2, padding_right=2, padding_bottom=2, padding_left=2
            )
            .no_borders()
        )

        # add invoice items
        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_columns=4,
            number_of_rows=len(self.__items) + 1 + 5,
            column_widths=[2, 1, 1, 1],
        )
        t.append_layout_element(
            Table.TableCell(
                Chunk("DESCRIPTION", font=Standard14Fonts.get("Helvetica-Bold")),
                background_color=A4PortraitInvoice.__LIGHT_GRAY,
            )
        )
        t.append_layout_element(
            Table.TableCell(
                Chunk("QUANTITY", font=Standard14Fonts.get("Helvetica-Bold")),
                background_color=A4PortraitInvoice.__LIGHT_GRAY,
            )
        )
        t.append_layout_element(
            Table.TableCell(
                Chunk(
                    "UNIT PRICE",
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                ),
                background_color=A4PortraitInvoice.__LIGHT_GRAY,
            )
        )
        t.append_layout_element(
            Table.TableCell(
                Chunk(
                    "AMOUNT",
                    font=Standard14Fonts.get("Helvetica-Bold"),
                    horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                ),
                background_color=A4PortraitInvoice.__LIGHT_GRAY,
            )
        )
        for a, d, q, u in self.__items:
            t.append_layout_element(Paragraph(d))
            t.append_layout_element(Chunk(f"{q}"))
            t.append_layout_element(
                Chunk(
                    f"{u} {self.__currency_abbreviation}",
                    horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                )
            )
            t.append_layout_element(
                Chunk(
                    f"{a} {self.__currency_abbreviation}",
                    horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                )
            )
        # empty row
        for _ in range(0, 4):
            t.append_layout_element(Chunk(" "))
        # subtotal
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(
            Chunk("Subtotal:", font=Standard14Fonts.get("Helvetica-Bold"))
        )
        t.append_layout_element(
            Chunk(
                f"{self.__subtotal} {self.__currency_abbreviation}",
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            )
        )
        # discounts
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(
            Chunk("Discounts:", font=Standard14Fonts.get("Helvetica-Bold"))
        )
        t.append_layout_element(
            Chunk(
                f"{self.__discounts} {self.__currency_abbreviation}",
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            )
        )
        # taxes
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(
            Chunk("Taxes:", font=Standard14Fonts.get("Helvetica-Bold"))
        )
        t.append_layout_element(
            Chunk(
                f"{self.__taxes} {self.__currency_abbreviation}",
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            )
        )
        # taxes
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(Chunk(" "))
        t.append_layout_element(
            Chunk("Total:", font=Standard14Fonts.get("Helvetica-Bold"))
        )
        t.append_layout_element(
            Chunk(
                f"{self.__total} {self.__currency_abbreviation}",
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            )
        )
        t.set_padding_on_all_cells(
            padding_top=2, padding_right=2, padding_bottom=2, padding_left=2
        )
        t.no_borders()
        layout.append_layout_element(t)

        # empty
        layout.append_layout_element(Chunk(" "))

        # terms and conditions
        Paragraph(
            self.__terms_and_conditions,
            text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            font_size=10,
            font_color=A4PortraitInvoice.__LIGHT_GRAY,
            padding_right=page.get_size()[0] // 10,
            padding_left=page.get_size()[0] // 10,
            padding_bottom=page.get_size()[1] // 20,
        ).paint(
            available_space=(0, 0, page.get_size()[0], page.get_size()[1]), page=page
        )

    #
    # PUBLIC
    #

    def append_item(
        self,
        amount: float,
        description: str,
        quantity: int,
        unit_price: float,
    ) -> "A4PortraitInvoice":
        """
        Append an item to the invoice.

        This method allows the user to add a line item to the invoice, which includes the item's total amount,
        description, quantity, and unit price. The item will be included in the invoice when it is generated.

        :param amount:      The total amount for the line item, calculated as quantity multiplied by unit price.
        :param description: A brief description of the item being invoiced.
        :param quantity:    The quantity of the item being billed.
        :param unit_price:  The price per unit of the item.
        :return:            The updated invoice object, allowing for method chaining.
        """
        self.__items += [(amount, description, quantity, unit_price)]
        return self

    def save(self, path: str) -> "A4PortraitInvoice":
        """
        Save the invoice to a specified file path.

        This method writes the current invoice document to the given file path.
        The document will be saved in the PDF format. If the file already exists,
        it may be overwritten.

        :param path:    The file path where the invoice will be saved.
        :return:        Self, allowing for method chaining.
        """
        self.__build()
        assert self.__document is not None
        PDF.write(what=self.__document, where_to=path)
        return self

    def set_address(
        self,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        address_line_4: str,
        address_line_5: str,
    ) -> "A4PortraitInvoice":
        """
        Set the user's company address for the invoice.

        This method allows the user to specify the company address that will be displayed
        on the invoice. The address is composed of up to five address lines.

        :param address_line_1:  The first line of the company address (typically the company name or primary identifier).
        :param address_line_2:  The second line of the company address (e.g., street address or P.O. Box).
        :param address_line_3:  The third line of the company address (e.g., city, state/province).
        :param address_line_4:  The fourth line of the company address (e.g., postal/ZIP code).
        :param address_line_5:  The fifth line of the company address (e.g., country).
        :return:                The updated invoice object, allowing for method chaining.
        """
        self.__address_lines = [
            address_line_1,
            address_line_2,
            address_line_3,
            address_line_4,
            address_line_5,
        ]
        return self

    def set_bill_to(
        self,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        address_line_4: str,
        address_line_5: str,
    ) -> "A4PortraitInvoice":
        """
        Set the 'Bill To' address for the invoice.

        This method allows the user to specify the billing address that will be displayed on the invoice,
        typically representing  the recipient or customer being billed.
        The address is composed of up to five address lines.

        :param address_line_1:  The first line of the billing address (typically the recipient's name or company name).
        :param address_line_2:  The second line of the billing address (e.g., street address or P.O. Box).
        :param address_line_3:  The third line of the billing address (e.g., city, state/province).
        :param address_line_4:  The fourth line of the billing address (e.g., postal/ZIP code).
        :param address_line_5:  The fifth line of the billing address (e.g., country).
        :return:                The updated in voice object, allowing for method chaining.
        """
        self.__bill_to_address_lines = [
            address_line_1,
            address_line_2,
            address_line_3,
            address_line_4,
            address_line_5,
        ]
        return self

    def set_currency_abbreviation(
        self, currency_abbreviation: str
    ) -> "A4PortraitInvoice":
        """
        Set the currency abbreviation for the invoice.

        This method allows the user to specify the currency abbreviation that will be displayed on the invoice.
        This is typically a three-letter code representing the currency (e.g., "USD" for United States Dollar,
        "EUR" for Euro).

        :param currency_abbreviation:   The currency abbreviation, represented as a string.
        :return:                        The updated invoice object, allowing for method chaining.
        """
        self.__currency_abbreviation = currency_abbreviation
        return self

    def set_date(self, date: datetime.datetime) -> "A4PortraitInvoice":
        """
        Set the date for the invoice.

        This method allows the user to specify the date that will be displayed on the invoice.
        The date should be provided as a `datetime.datetime` object.

        :param date:    The date to set for the invoice, represented as a `datetime.datetime` object.
        :return:        The updated invoice object, allowing for method chaining.
        """
        self.__date = date
        return self

    def set_discounts(self, discounts: float) -> "A4PortraitInvoice":
        """
        Set the discount amount for the invoice.

        This method allows the user to specify the total discount to be applied to the invoice.
        The discount should be provided as a floating-point number, representing a flat amount.

        :param discounts:   The discount amount to apply to the invoice, represented as a float.
        :return:            The updated invoice object, allowing for method chaining.
        """
        self.__discounts = discounts
        return self

    def set_due_date(self, due_date: datetime.datetime) -> "A4PortraitInvoice":
        """
        Set the due date for the invoice.

        This method allows the user to specify the due date that will be displayed on the invoice.
        The due date should be provided as a `datetime.datetime` object.

        :param due_date:    The due date to set for the invoice, represented as a `datetime.datetime` object.
        :return:            The updated invoice object, allowing for method chaining.
        """
        self.__due_date = due_date
        return self

    def set_invoice_nr(self, invoice_nr: str) -> "A4PortraitInvoice":
        """
        Set the invoice number.

        This method allows the user to specify a unique invoice number that will be displayed on the invoice.
        The invoice number is typically used for tracking and reference purposes.

        :param invoice_nr:  The unique invoice number, represented as a string.
        :return:            The updated invoice object, allowing for method chaining.
        """
        self.__invoice_nr = invoice_nr
        return self

    def set_logo(
        self,
        bytes_path_pil_image_or_url: typing.Union[  # type: ignore[name-defined]
            bytes, pathlib.Path, "PIL.Image.Image", str  # type: ignore[name-defined]
        ],
    ) -> "A4PortraitInvoice":
        """
        Set the logo for the invoice.

        This method allows the user to specify the logo that will be displayed on the invoice. The logo can be provided
        in various formats, including raw image bytes, a file path, a Pillow (PIL) Image object, or a URL.

        :param bytes_path_pil_image_or_url: The logo image to set. It can be provided in one of the following formats:
            - `bytes`: The raw byte content of the image.
            - `pathlib.Path`: The path to the image file.
            - `PIL.Image.Image`: A Pillow image object.
            - `str`: A URL pointing to the image.
        :return: The updated invoice object, allowing for method chaining.
        """
        self.__logo = bytes_path_pil_image_or_url
        return self

    def set_ship_to(
        self,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        address_line_4: str,
        address_line_5: str,
    ) -> "A4PortraitInvoice":
        """
        Set the 'Ship To' address for the invoice.

        This method allows the user to specify the shipping address that will be displayed on the invoice,
        representing the location where the goods or services are to be delivered.
        The address is composed of up to five address lines.

        :param address_line_1:  The first line of the shipping address (typically the recipient's name or company name).
        :param address_line_2:  The second line of the shipping address (e.g., street address or P.O. Box).
        :param address_line_3:  The third line of the shipping address (e.g., city, state/province).
        :param address_line_4:  The fourth line of the shipping address (e.g., postal/ZIP code).
        :param address_line_5:  The fifth line of the shipping address (e.g., country).
        :return:                The updated invoice object, allowing for method chaining.
        """
        self.__ship_to_address_lines = [
            address_line_1,
            address_line_2,
            address_line_3,
            address_line_4,
            address_line_5,
        ]
        return self

    def set_subtotal(self, subtotal: float) -> "A4PortraitInvoice":
        """
        Set the subtotal amount for the invoice.

        This method allows the user to specify the subtotal for the invoice,
        which is the total amount before any taxes or discounts are applied.
        The subtotal should be provided as a floating-point number.

        :param subtotal:    The subtotal amount for the invoice, represented as a float.
        :return:            The updated invoice object, allowing for method chaining.
        """
        self.__subtotal = subtotal
        return self

    def set_taxes(self, taxes: float) -> "A4PortraitInvoice":
        """
        Set the tax amount for the invoice.

        This method allows the user to specify the total tax to be applied to the invoice.
        The tax should be provided as a floating-point number,
        representing the total tax amount calculated based on the subtotal and any applicable tax rates.

        :param taxes:   The tax amount to apply to the invoice, represented as a float.
        :return:        The updated invoice object, allowing for method chaining.
        """
        self.__taxes = taxes
        return self

    def set_terms_and_conditions(
        self, terms_and_conditions: str
    ) -> "A4PortraitInvoice":
        """
        Set the terms and conditions for the invoice.

        This method allows the user to specify the terms and conditions that will be displayed on the invoice.
        This may include payment terms, refund policies, or any other relevant conditions that the recipient
        should be aware of. The terms and conditions should be provided as a string.

        :param terms_and_conditions:    The terms and conditions to display on the invoice, represented as a string.
        :return:                        The updated invoice object, allowing for method chaining.
        """
        self.__terms_and_conditions = terms_and_conditions
        return self

    def set_total(self, total: float) -> "A4PortraitInvoice":
        """
        Set the total amount for the invoice.

        This method allows the user to specify the total amount for the invoice, which includes the subtotal,
        taxes, and any applicable discounts. The total should be provided as a floating-point number.

        :param total:   The total amount for the invoice, represented as a float.
        :return:        The updated invoice object, allowing for method chaining.
        """
        self.__total = total
        return self
