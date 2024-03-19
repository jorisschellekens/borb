#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of FormField represents a text area.
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
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.forms.form_field import FormField
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.page.page import Page


class TextArea(FormField):
    """
    This implementation of FormField represents a text area.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = True,
        border_color: Color = HexColor("808080"),
        border_left: bool = True,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = True,
        border_top: bool = True,
        border_width: Decimal = Decimal(1),
        default_value: str = "",
        field_name: typing.Optional[str] = None,
        font_color: Color = HexColor("000000"),
        font_size: typing.Optional[Decimal] = Decimal(12),
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        number_of_lines: int = 5,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        value: str = "",
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(TextArea, self).__init__(
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
        assert number_of_lines > 0
        self._font_color = font_color
        self._value: str = value
        self._default_value: str = default_value
        self._number_of_lines: int = number_of_lines
        self._field_name: typing.Optional[str] = field_name
        self._widget_dictionary: typing.Optional[Dictionary] = None

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        assert self._font_size is not None
        line_height: Decimal = self._font_size * Decimal(1.2)
        return Rectangle(
            available_space.get_x(),
            available_space.get_y()
            + available_space.get_height()
            - line_height * self._number_of_lines,
            max(available_space.get_width(), Decimal(64)),
            line_height * self._number_of_lines,
        )

    def _init_widget_dictionary(self, page: Page, layout_box: Rectangle) -> None:
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

        # widget normal appearance
        widget_normal_appearance: Stream = Stream()
        widget_normal_appearance.set_is_unique(True)
        widget_normal_appearance[Name("Type")] = Name("XObject")
        widget_normal_appearance[Name("Subtype")] = Name("Form")
        widget_normal_appearance[Name("BBox")] = List().set_is_inline(True)
        widget_normal_appearance["BBox"].append(bDecimal(0))
        widget_normal_appearance["BBox"].append(bDecimal(0))
        widget_normal_appearance["BBox"].append(bDecimal(layout_box.width))
        widget_normal_appearance["BBox"].append(
            bDecimal((self._font_size + 1) * self._number_of_lines)
        )
        widget_normal_appearance[Name("Resources")] = widget_resources
        bts = b"/Tx BMC EMC"
        widget_normal_appearance[Name("DecodedBytes")] = bts
        widget_normal_appearance[Name("Bytes")] = zlib.compress(bts, 9)
        widget_normal_appearance[Name("Filter")] = Name("FlateDecode")
        widget_normal_appearance[Name("Length")] = bDecimal(len(bts))

        # widget appearance dictionary
        widget_appearance_dictionary: Dictionary = Dictionary()
        widget_appearance_dictionary.set_is_unique(True)
        widget_appearance_dictionary[Name("N")] = widget_normal_appearance

        # get Catalog
        catalog: Dictionary = root["XRef"]["Trailer"]["Root"]  # type: ignore[attr-defined]

        # widget dictionary
        # fmt: off
        self._widget_dictionary = Dictionary()
        self._widget_dictionary.set_is_unique(True)
        self._widget_dictionary[Name("Type")] = Name("Annot")
        self._widget_dictionary[Name("Subtype")] = Name("Widget")
        self._widget_dictionary[Name("F")] = bDecimal(4)
        self._widget_dictionary[Name("Rect")] = List().set_is_inline(True)
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.x))
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.y + layout_box.height - (self._font_size + 1) * self._number_of_lines))
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.x + layout_box.width))
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.y + layout_box.height))
        self._widget_dictionary[Name("FT")] = Name("Tx")
        self._widget_dictionary[Name("Ff")] = bDecimal(4096)
        self._widget_dictionary[Name("P")] = catalog
        self._widget_dictionary[Name("T")] = String(self._field_name or self._get_auto_generated_field_name(page))
        self._widget_dictionary[Name("V")] = String(self._value)
        self._widget_dictionary[Name("DV")] = String(self._default_value)
        self._widget_dictionary[Name("DR")] = widget_resources
        # fmt: on

        # rendering instructions
        font_color_rgb: RGBColor = self._font_color.to_rgb()
        self._widget_dictionary[Name("DA")] = String(
            "%f %f %f rg /%s %f Tf"
            % (
                float(font_color_rgb.red),
                float(font_color_rgb.green),
                float(font_color_rgb.blue),
                font_resource_name,
                float(self._font_size),
            )
        )
        self._widget_dictionary[Name("AP")] = widget_appearance_dictionary

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
        # determine layout rectangle
        cbox: Rectangle = self._get_content_box(available_space)

        # init self._widget_dictionary
        self._init_widget_dictionary(page, cbox)

        # set location
        # fmt: off
        assert self._font_size is not None
        if self._widget_dictionary is not None:
            self._widget_dictionary["AP"]["N"]["BBox"][2] = bDecimal(cbox.get_width())
            self._widget_dictionary["AP"]["N"]["BBox"][3] = bDecimal(self._font_size)
            self._widget_dictionary["Rect"][0] = bDecimal(cbox.get_x())
            self._widget_dictionary["Rect"][1] = bDecimal(cbox.get_y())
            self._widget_dictionary["Rect"][2] = bDecimal(cbox.get_x() + cbox.get_width())
            self._widget_dictionary["Rect"][3] = bDecimal(cbox.get_y() + cbox.get_height())
        # fmt: on

    #
    # PUBLIC
    #
