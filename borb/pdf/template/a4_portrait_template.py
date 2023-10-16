#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a PDF document
"""
import io
import typing
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.image.barcode import Barcode
from borb.pdf.canvas.layout.image.barcode import BarcodeType
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.table.table_util import TableUtil
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document as bDocument
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class A4PortraitTemplate:
    """
    This class represents an A4 portrait PDF document
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        # empty Document
        self._document: bDocument = bDocument()

        # empty Page
        self._page: Page = Page()
        self._document.add_page(self._page)

        # layout
        self._layout: PageLayout = SingleColumnLayout(self._page)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def add_blank_page(self) -> "A4PortraitTemplate":
        """
        This function adds a blank Page to this A4PortraitTemplate,
        and then switches to a new Page
        :return:    self
        """
        assert isinstance(self._layout, SingleColumnLayout)
        self._layout.switch_to_next_page()
        self._layout.switch_to_next_page()
        return self

    def add_h1(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 1 heading to this A4PortraitTemplate
        :param text:    the text of the (level 1) heading
        :return:        self
        """
        return self.add_heading(
            text=text,
            font_color_as_hex="#8bbd8b",
            font_family="Helvetica",
            font_size=16,
            level=0,
        )

    def add_h2(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 2 heading to this A4PortraitTemplate
        :param text:    the text of the (level 2) heading
        :return:        self
        """
        return self.add_heading(
            text=text,
            font_color_as_hex="#8bbd8b",
            font_family="Helvetica",
            font_size=13,
            level=1,
        )

    def add_h3(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 3 heading to this A4PortraitTemplate
        :param text:    the text of the (level 3) heading
        :return:        self
        """
        return self.add_heading(
            text=text,
            font_color_as_hex="#6cae75",
            font_family="Helvetica",
            font_size=12,
            level=2,
        )

    def add_h4(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 4 heading to this A4PortraitTemplate
        :param text:    the text of the (level 4) heading
        :return:        self
        """
        return self.add_heading(
            text=text,
            font_color_as_hex="#8bbd8b",
            font_family="Helvetica-Oblique",
            font_size=11,
            level=3,
        )

    def add_h5(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 5 heading to this A4PortraitTemplate
        :param text:    the text of the (level 5) heading
        :return:        self
        """
        return self.add_heading(
            text=text,
            font_color_as_hex="#8bbd8b",
            font_family="Helvetica",
            font_size=11,
            level=4,
        )

    def add_h6(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 6 heading to this A4PortraitTemplate
        :param text:    the text of the (level 6) heading
        :return:        self
        """
        return self.add_heading(
            text=text,
            font_color_as_hex="#6cae75",
            font_family="Helvetica",
            font_size=11,
            level=5,
        )

    def add_heading(
        self,
        text: str,
        font_color_as_hex: str = "#000000",
        font_family: str = "Helvetica",
        font_size: int = 12,
        level: int = 1,
    ) -> "A4PortraitTemplate":
        """
        This function adds a Heading of text to this A4PortraitTemplate
        :param text:                    the text (str) to be added
        :param font_color_as_hex:       the font-color (hex str) of the text to be added
        :param font_family:             the font-family (str) of the text to be added
        :param font_size:               the font-size (int) of the text to be added
        :param level:                   the outline level (int) of the text to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, str),               "text must be str"
        assert isinstance(font_color_as_hex, str),  "font_color_as_hex must be str"
        assert len(font_color_as_hex) == 7,         "font_color_as_hex must be 7 characters long"
        assert font_color_as_hex[0] == '#',         "font_color_as_hex must start with #"
        assert isinstance(font_family, str),        "font_family must be str"
        assert isinstance(font_size, int),          "font size must be int"
        assert font_size >= 1,                      "font_size must be larger than or equal to 1"
        assert level >= 0
        # fmt: on
        self._layout.add(
            Heading(
                text,
                outline_level=level,
                font=font_family,
                font_size=Decimal(font_size),
                font_color=HexColor(font_color_as_hex),
            )
        )
        return self

    def add_image(
        self,
        url_or_path: typing.Union[str, Path],
        width: typing.Optional[int],
        height: typing.Optional[int],
    ) -> "A4PortraitTemplate":
        """
        This function adds an Image to this A4PortraitTemplate
        :param url_or_path:     the url (str) or path (Path) of the Image
        :param width:           the desired width (int) of the Image
        :param height:          the desired height (int) of the Image
        :return:                self
        """
        assert height is None or (isinstance(height, int) and height >= 0)
        assert width is None or (isinstance(width, int) and width >= 0)
        assert isinstance(url_or_path, str) or isinstance(url_or_path, Path)

        # convert to typing.Optional[Decimal]
        # fmt: off
        width_as_decimal: typing.Optional[Decimal] = (None if width is None else Decimal(width))
        height_as_decimal: typing.Optional[Decimal] = (None if height is None else Decimal(height))
        # fmt: on

        if isinstance(url_or_path, str):
            self._layout.add(
                Image(url_or_path, height=height_as_decimal, width=width_as_decimal)
            )
        if isinstance(url_or_path, Path):
            assert url_or_path.exists()
            self._layout.add(
                Image(url_or_path, height=height_as_decimal, width=width_as_decimal)
            )
        return self

    def add_ordered_list(
        self,
        text: typing.List[str],
        font_color_as_hex: str = "#000000",
        font_family: str = "Helvetica",
        font_size: int = 12,
    ) -> "A4PortraitTemplate":
        """
        This function adds an OrderedList of str(s) to this A4PortraitTemplate
        :param text:                    the text (typing.List[str]) to be added
        :param font_color_as_hex:       the font-color (hex str) of the text to be added
        :param font_family:             the font-family (str) of the text to be added
        :param font_size:               the font-size (int) of the text to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, typing.List),           "text must be typing.List[str]"
        assert len(text) > 0,                           "text must have 1 or more element(s)"
        assert all([isinstance(x, str) for x in text]), "text must be typing.List[str]"
        assert isinstance(font_color_as_hex, str),      "font_color_as_hex must be str"
        assert len(font_color_as_hex) == 7,             "font_color_as_hex must be 7 characters long"
        assert font_color_as_hex[0] == '#',             "font_color_as_hex must start with #"
        assert isinstance(font_family, str),            "font_family must be str"
        assert isinstance(font_size, int),              "font_size must be int"
        assert font_size >= 1,                          "font_size must be larger than or equal to 1"
        # fmt: on
        l: OrderedList = OrderedList()
        for x in text:
            l.add(
                Paragraph(
                    x,
                    font=font_family,
                    font_size=Decimal(font_size),
                    font_color=HexColor(font_color_as_hex),
                )
            )
        self._layout.add(l)
        return self

    def add_page(self) -> "A4PortraitTemplate":
        """
        This function switches to a new Page
        :return:    self
        """
        assert isinstance(self._layout, SingleColumnLayout)
        self._layout.switch_to_next_page()
        return self

    def add_qr_code(
        self,
        text: str,
        fill_color_as_hex: str = "#ffffff",
        height: typing.Optional[int] = None,
        stroke_color_as_hex: str = "#000000",
        width: typing.Optional[int] = None,
    ) -> "A4PortraitTemplate":
        """
        This function adds a QR code to this A4PortraitTemplate
        :param text:                    the text in the QR code
        :param fill_color_as_hex:       the fill-color (as hex str) of the QR code to be added
        :param height:                  the height of the QR code to be added
        :param stroke_color_as_hex:     the stroke-color (as hex str) of the QR code to be added
        :param width:                   the width of the QR code to be added
        :return:                        self
        """
        assert (
            len(fill_color_as_hex) == 7
        ), "fill_color_as_hex must be 7 characters long"
        assert fill_color_as_hex[0] == "#", "fill_color_as_hex must start with #"
        assert height is None or (isinstance(height, int) and height >= 0)
        assert (
            len(stroke_color_as_hex) == 7
        ), "stroke_color_as_hex must be 7 characters long"
        assert stroke_color_as_hex[0] == "#", "stroke_color_as_hex must start with #"
        assert width is None or (isinstance(width, int) and width >= 0)

        # convert to typing.Optional[Decimal]
        # fmt: off
        width_as_decimal: typing.Optional[Decimal] = (None if width is None else Decimal(width))
        height_as_decimal: typing.Optional[Decimal] = (None if height is None else Decimal(height))
        # fmt: on

        self._layout.add(
            Barcode(
                data=text,
                stroke_color=HexColor(stroke_color_as_hex),
                fill_color=HexColor(fill_color_as_hex),
                width=width_as_decimal,
                height=height_as_decimal,
                type=BarcodeType.QR,
            )
        )
        return self

    def add_table(
        self,
        text: typing.List[typing.List[str]],
        font_color_as_hex: str = "#000000",
        font_family: str = "Helvetica",
        font_size: int = 12,
        use_header_row: bool = True,
        use_header_column: bool = False,
    ) -> "A4PortraitTemplate":
        """
        This function adds a Table to this A4PortraitTemplate
        :param text:                the text (typing.List[typing.List[str]]) in the Table
        :param font_color_as_hex:   the font-color (hex str) of the text to be added
        :param font_family:         the font-family (str) of the text to be added
        :param font_size:           the font-size (int) of the text to be added
        :param use_header_row:      whether to use a header row or not (default True)
        :param use_header_column:   whether to use a header column or not (default False)
        :return:                    self
        """
        # fmt: off

        assert isinstance(text, typing.List),                   "text must be typing.List[typing.List[str]]"
        assert len(text) > 0,                                   "text must have 1 or more element(s)"
        assert all([isinstance(x, typing.List) for x in text]), "text must be typing.List[typing.List[str]]"
        assert isinstance(font_color_as_hex, str),              "font_color_as_hex must be str"
        assert len(font_color_as_hex) == 7,                     "font_color_as_hex must be 7 characters long"
        assert font_color_as_hex[0] == '#',                     "font_color_as_hex must start with #"
        assert isinstance(font_family, str),                    "font_family must be str"
        assert isinstance(font_size, int),                      "font_size must be int"
        assert font_size >= 1,                                  "font_size must be larger than or equal to 1"
        # fmt: on
        t: Table = TableUtil.from_2d_array(
            text,
            font_size=Decimal(font_size),
            header_row=use_header_row,
            header_col=use_header_column,
            round_to_n_digits=2,
            flexible_column_width=False,
        )

        # modify all Paragraph objects in Table
        for tc in t._content:
            assert isinstance(tc._layout_element, Paragraph)
            p: Paragraph = tc._layout_element
            p._font_color = HexColor(font_color_as_hex)
            p._font = StandardType1Font(font_family)
        # add Table to SingleColumnLayout
        self._layout.add(t)

        # return
        return self

    def add_text(
        self,
        text: str,
        font_color_as_hex: str = "#000000",
        font_family: str = "Helvetica",
        font_size: int = 12,
    ) -> "A4PortraitTemplate":
        """
        This function adds a Paragraph of text to this A4PortraitTemplate
        :param text:                    the text (str) to be added
        :param font_color_as_hex:       the font-color (hex str) of the text to be added
        :param font_family:             the font-family (str) of the text to be added
        :param font_size:               the font-size (int) of the text to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, str),               "text must be str"
        assert isinstance(font_color_as_hex, str),  "font_color_as_hex must be str"
        assert len(font_color_as_hex) == 7,         "font_color_as_hex must be 7 characters long"
        assert font_color_as_hex[0] == '#',         "font_color_as_hex must start with #"
        assert isinstance(font_family, str),        "font_family must be str"
        assert isinstance(font_size, int),          "font size must be int"
        assert font_size >= 1,                      "font_size must be larger than or equal to 1"
        # fmt: on
        self._layout.add(
            Paragraph(
                text,
                font=font_family,
                font_size=Decimal(font_size),
                font_color=HexColor(font_color_as_hex),
            )
        )
        return self

    def add_unordered_list(
        self,
        text: typing.List[str],
        font_color_as_hex: str = "#000000",
        font_family: str = "Helvetica",
        font_size: int = 12,
    ) -> "A4PortraitTemplate":
        """
        This function adds an UnorderedList of str(s) to this A4PortraitTemplate
        :param text:                    the text (typing.List[str]) to be added
        :param font_color_as_hex:       the font-color (hex str) of the text to be added
        :param font_family:             the font-family (str) of the text to be added
        :param font_size:               the font-size (int) of the text to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, typing.List),           "text must be typing.List[str]"
        assert len(text) > 0,                           "text must have 1 or more element(s)"
        assert all([isinstance(x, str) for x in text]), "text must be typing.List[str]"
        assert isinstance(font_color_as_hex, str),      "font_color_as_hex must be str"
        assert len(font_color_as_hex) == 7,             "font_color_as_hex must be 7 characters long"
        assert font_color_as_hex[0] == '#',             "font_color_as_hex must start with #"
        assert isinstance(font_family, str),            "font_family must be str"
        assert isinstance(font_size, int),              "font_size must be int"
        assert font_size >= 1,                          "font_size must be larger than or equal to 1"
        # fmt: on
        l: UnorderedList = UnorderedList()
        for x in text:
            l.add(
                Paragraph(
                    x,
                    font=font_family,
                    font_size=Decimal(font_size),
                    font_color=HexColor(font_color_as_hex),
                )
            )
        self._layout.add(l)
        return self

    def bytes(self) -> bytes:
        """
        This function returns the bytes representing this A4PortraitTemplate.
        It does so by saving this A4PortraitTemplate to an io.BytesIO buffer,
        and returning its bytes.
        :return:    the bytes representing this A4PortraitTemplate
        """
        buffer = io.BytesIO()
        PDF.dumps(buffer, self._document)
        buffer.seek(0)
        return buffer.getvalue()

    def save(self, path_or_str: typing.Union[str, Path]) -> "A4PortraitTemplate":
        """
        This function stores this A4PortraitTemplate at the given path
        :param path_or_str:     the path or str representing the location at which to store this A4PortraitTemplate
        :return:                self
        """
        with open(path_or_str, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self._document)
        return self
