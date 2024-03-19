#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of FormField represents a push button.
"""
import typing
import zlib
from decimal import Decimal

from borb.io.read.pdf_object import PDFObject
from borb.io.read.types import Boolean
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import Stream
from borb.io.read.types import String
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.forms.form_field import FormField
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.page.page import Page


class PushButton(FormField):
    """
    This implementation of FormField represents a push button.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        background_color: typing.Optional[Color] = HexColor("efefef"),
        border_bottom: bool = True,
        border_color: Color = HexColor("767676"),
        border_left: bool = True,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = True,
        border_top: bool = True,
        border_width: Decimal = Decimal(1),
        field_name: typing.Optional[str] = None,
        font_size: typing.Optional[Decimal] = Decimal(12),
        font_color: Color = HexColor("000000"),
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        padding_bottom: Decimal = Decimal(2),
        padding_left: Decimal = Decimal(6),
        padding_right: Decimal = Decimal(6),
        padding_top: Decimal = Decimal(2),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(PushButton, self).__init__(
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            font="Helvetica",
            font_color=font_color,
            font_size=font_size,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        assert len(text) > 0
        self._field_name: typing.Optional[str] = field_name
        self._text = text
        self._widget_dictionary: typing.Optional[Dictionary] = None

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        assert self._font_size is not None
        line_of_text: LineOfText = LineOfText(
            self._text,
            background_color=self._background_color,
            font_size=self._font_size,
            font_color=self._font_color,
        )
        return line_of_text.get_layout_box(available_space)

    def _init_widget_dictionary(self, page: Page) -> None:
        if self._widget_dictionary is not None:
            return

        root: typing.Optional[PDFObject] = page.get_root()
        assert root is not None
        assert isinstance(root, Dictionary)
        if "XRef" not in root:
            return

        # init page and font resources
        assert self._font_size is not None
        font_resource_name: Name = self._get_font_resource_name(
            StandardType1Font("Helvetica"), page
        )

        # widget resource dictionary
        widget_resources: Dictionary = Dictionary()
        widget_resources.set_is_unique(True)
        widget_resources[Name("Font")] = page["Resources"]["Font"]

        # get Catalog
        catalog: Dictionary = root["XRef"]["Trailer"]["Root"]

        # widget dictionary
        # fmt: off
        self._widget_dictionary = Dictionary()
        self._widget_dictionary.set_is_unique(True)
        self._widget_dictionary[Name("AA")] = Dictionary()
        self._widget_dictionary[Name("AA")][Name("D")] = Dictionary()
        self._widget_dictionary[Name("AA")][Name("D")][Name("Type")] = Name("Action")
        self._widget_dictionary[Name("AA")][Name("D")][Name("S")] = Name("ResetForm")
        # fmt: on

        # create normal appearance
        # fmt: off
        self._widget_dictionary[Name("AP")] = Dictionary()
        self._widget_dictionary[Name("AP")].set_is_unique(True)
        self._widget_dictionary[Name("AP")][Name("N")] = Stream()
        self._widget_dictionary[Name("AP")][Name("N")][Name("Type")] = Name("XObject")
        self._widget_dictionary[Name("AP")][Name("N")][Name("Subtype")] = Name("Form")
        self._widget_dictionary[Name("AP")][Name("N")][Name("BBox")] = List().set_is_inline(True)
        for _ in range(0, 4):
            self._widget_dictionary[Name("AP")][Name("N")][Name("BBox")].append(bDecimal(0))
        self._widget_dictionary[Name("AP")][Name("N")][Name("DecodedBytes")] = b"/Tx BMC EMC"
        self._widget_dictionary[Name("AP")][Name("N")][Name("Bytes")] = zlib.compress(self._widget_dictionary[Name("AP")][Name("N")][Name("DecodedBytes")], 9)
        self._widget_dictionary[Name("AP")][Name("N")][Name("Filter")] = Name("FlateDecode")
        self._widget_dictionary[Name("AP")][Name("N")][Name("Length")] = bDecimal(len(self._widget_dictionary[Name("AP")][Name("N")][Name("Bytes")]))
        self._widget_dictionary[Name("AP")][Name("N")][Name("Resources")] = Dictionary()
        self._widget_dictionary[Name("AP")][Name("N")][Name("Resources")][Name("ProcSet")] = List().set_is_inline(True)
        self._widget_dictionary[Name("AP")][Name("N")][Name("Resources")][Name("ProcSet")].append(Name("PDF"))
        self._widget_dictionary[Name("AP")][Name("N")][Name("Resources")][Name("ProcSet")].append(Name("Text"))
        self._widget_dictionary[Name("AP")][Name("N")][Name("Resources")][Name("Font")] = Dictionary()
        self._widget_dictionary[Name("AP")][Name("N")][Name("Resources")][Name("Font")] = page["Resources"]["Font"]
        # fmt: on

        # create default appearance
        # fmt: off
        self._widget_dictionary[Name("DA")] = String("0.23921 0.23921 0.23921 rg /%s %f Tf" % (font_resource_name, float(self._font_size)))
        self._widget_dictionary[Name("DR")] = widget_resources
        # fmt: on

        # other flags
        # fmt: off
        self._widget_dictionary[Name("F")] = bDecimal(4)
        self._widget_dictionary[Name("Ff")] = bDecimal(65536)
        self._widget_dictionary[Name("FT")] = Name("Btn")
        self._widget_dictionary[Name("MK")] = Dictionary()
        self._widget_dictionary[Name("MK")][Name("BC")] = List().set_is_inline(True)
        self._widget_dictionary[Name("MK")][Name("BG")] = List().set_is_inline(True)
        self._widget_dictionary[Name("MK")][Name("CA")] = String("")
        self._widget_dictionary[Name("P")] = catalog
        self._widget_dictionary[Name("Q")] = bDecimal(1)
        self._widget_dictionary[Name("Rect")] = List().set_is_inline(True)
        for _ in range(0, 4):
            self._widget_dictionary[Name("Rect")].append(bDecimal(0))
        self._widget_dictionary[Name("Subtype")] = Name("Widget")
        self._widget_dictionary[Name("T")] = String(self._field_name or self._get_auto_generated_field_name(page))
        self._widget_dictionary[Name("Type")] = Name("Annot")
        # fmt: on

        # append field to page /Annots
        if "Annots" not in page:
            page[Name("Annots")] = List()
        page["Annots"].append(self._widget_dictionary)

        # append field to catalog
        if "AcroForm" not in catalog:
            catalog[Name("AcroForm")] = Dictionary()
            catalog["AcroForm"][Name("Fields")] = List()
            catalog["AcroForm"][Name("DR")] = widget_resources
            catalog["AcroForm"][Name("NeedAppearances")] = Boolean(True)
        catalog["AcroForm"]["Fields"].append(self._widget_dictionary)

    def _paint_content_box(self, page: "Page", available_space: Rectangle) -> None:
        # init self._widget_dictionary
        self._init_widget_dictionary(page)

        # layout text
        assert self._font_size is not None
        line_of_text = LineOfText(
            self._text,
            background_color=self._background_color,
            font_size=self._font_size,
            font_color=self._font_color,
        )
        line_of_text.paint(page, self._get_content_box(available_space))
        cbox: typing.Optional[Rectangle] = line_of_text.get_previous_paint_box()
        assert cbox is not None

        # add our own margins to expand the clickable part
        cbox.x -= self._padding_left
        cbox.width += self._padding_left + self._padding_right
        cbox.y -= self._padding_bottom
        cbox.height += self._padding_bottom + self._padding_top

        # set location
        # fmt: off
        if self._widget_dictionary is not None:
            self._widget_dictionary["Rect"][0] = bDecimal(cbox.get_x())                             # ll_x
            self._widget_dictionary["Rect"][1] = bDecimal(cbox.get_y())                             # ll_y
            self._widget_dictionary["Rect"][2] = bDecimal(cbox.get_x() + cbox.get_width())          # ur_x
            self._widget_dictionary["Rect"][3] = bDecimal(cbox.get_y() + cbox.get_height())         # ur_y
        # fmt: on

    #
    # PUBLIC
    #


class JavaScriptPushButton(PushButton):
    """
    This implementation of FormField represents a push button that triggers JavaScript.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        javascript: str,
        text: str,
        background_color: typing.Optional[Color] = HexColor("efefef"),
        border_bottom: bool = True,
        border_color: Color = HexColor("767676"),
        border_left: bool = True,
        border_right: bool = True,
        border_top: bool = True,
        border_width: Decimal = Decimal(1),
        field_name: typing.Optional[str] = None,
        font_size: typing.Optional[Decimal] = Decimal(12),
        font_color: Color = HexColor("000000"),
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: Decimal = Decimal(0),
        margin_left: Decimal = Decimal(0),
        margin_right: Decimal = Decimal(0),
        margin_top: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(2),
        padding_left: Decimal = Decimal(6),
        padding_right: Decimal = Decimal(6),
        padding_top: Decimal = Decimal(2),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(JavaScriptPushButton, self).__init__(
            text=text,
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            field_name=field_name,
            font_size=font_size,
            font_color=font_color,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self._javascript: str = javascript

    #
    # PRIVATE
    #

    def _init_widget_dictionary(self, page: Page) -> None:
        # call to super
        super(JavaScriptPushButton, self)._init_widget_dictionary(page)

        # build JavaScript stream object
        # fmt: off
        javascript_stream = Stream()
        javascript_stream.set_is_unique(True)
        javascript_stream[Name("Type")] = Name("JavaScript")
        javascript_stream[Name("DecodedBytes")] = bytes(self._javascript, "latin1")
        javascript_stream[Name("Bytes")] = zlib.compress(javascript_stream[Name("DecodedBytes")], 9)
        javascript_stream[Name("Length")] = bDecimal(len(javascript_stream[Name("Bytes")]))
        javascript_stream[Name("Filter")] = Name("FlateDecode")
        # fmt: on

        # modify action dictionary of PushButton (super)
        # fmt: off
        if self._widget_dictionary is not None:
            self._widget_dictionary[Name("AA")][Name("D")][Name("S")] = Name("JavaScript")
            self._widget_dictionary[Name("AA")][Name("D")][Name("JS")] = javascript_stream
        # fmt: on

    #
    # PUBLIC
    #
