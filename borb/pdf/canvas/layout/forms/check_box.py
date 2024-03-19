#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of FormField represents a text field.
"""
import copy
import typing
import zlib
from decimal import Decimal

from borb.io.read.pdf_object import PDFObject
from borb.io.read.types import Boolean
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List as bList
from borb.io.read.types import Name
from borb.io.read.types import Stream
from borb.io.read.types import String
from borb.io.read.types import String as bString
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.forms.form_field import FormField
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.page.page import Page


class CheckBox(FormField):
    """
    This implementation of FormField represents a text field.
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
        field_name: typing.Optional[str] = None,
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(12),
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(CheckBox, self).__init__(
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
        self._field_name: typing.Optional[str] = field_name
        self._widget_dictionary: typing.Optional[Dictionary] = None

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        assert self._font_size is not None
        line_height: Decimal = self._font_size * Decimal(1.2)
        return Rectangle(
            available_space.x,
            available_space.y + available_space.height - line_height,
            min(available_space.get_width(), self._font_size),
            line_height,
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
            StandardType1Font("Zapfdingbats"), page
        )

        # widget resource dictionary
        widget_resources: Dictionary = Dictionary()
        widget_resources[Name("Font")] = page["Resources"]["Font"]

        # widget "Off" appearance
        bts: bytes = bytes("/Tx BMC EMC", "latin1")
        widget_off_appearance: Stream = Stream()
        widget_off_appearance[Name("BBox")] = bList()
        widget_off_appearance[Name("BBox")].set_is_inline(True)
        widget_off_appearance[Name("BBox")].append(bDecimal(0))
        widget_off_appearance[Name("BBox")].append(bDecimal(0))
        widget_off_appearance[Name("BBox")].append(bDecimal(layout_box.width))
        widget_off_appearance[Name("BBox")].append(bDecimal(self._font_size))
        widget_off_appearance[Name("Bytes")] = zlib.compress(bts, 9)
        widget_off_appearance[Name("DecodedBytes")] = bts
        widget_off_appearance[Name("Filter")] = Name("FlateDecode")
        widget_off_appearance[Name("Length")] = bDecimal(len(bts))
        widget_off_appearance[Name("ProcSet")] = bList()
        widget_off_appearance[Name("ProcSet")].set_is_inline(True)
        widget_off_appearance[Name("ProcSet")].append(Name("PDF"))
        widget_off_appearance[Name("ProcSet")].append(Name("Text"))
        widget_off_appearance[Name("Resources")] = widget_resources
        widget_off_appearance[Name("Subtype")] = Name("Form")
        widget_off_appearance[Name("Type")] = Name("XObject")

        # widget "Yes" appearance
        bts = bytes(
            "/Tx BMC q BT 0 0 0 rg /%s 12 Tf 0 0 Td (8) Tj ET Q EMC"
            % font_resource_name,
            "latin1",
        )
        widget_yes_appearance: Stream = copy.deepcopy(widget_off_appearance)
        widget_yes_appearance[Name("Bytes")] = zlib.compress(bts, 9)
        widget_yes_appearance[Name("DecodedBytes")] = bts
        widget_yes_appearance[Name("Filter")] = Name("FlateDecode")
        widget_yes_appearance[Name("Length")] = bDecimal(len(bts))

        # widget normal appearance
        widget_normal_appearance: Dictionary = Dictionary()
        widget_normal_appearance[Name("Off")] = widget_off_appearance
        widget_normal_appearance[Name("Yes")] = widget_yes_appearance

        # widget appearance dictionary
        widget_appearance_dictionary: Dictionary = Dictionary()
        widget_appearance_dictionary[Name("N")] = widget_normal_appearance
        widget_appearance_dictionary.set_is_unique(True)

        # get Catalog
        catalog: Dictionary = root["XRef"]["Trailer"]["Root"]  # type: ignore [attr-defined]

        # get font_color (in RGB model)
        font_color_rgb: RGBColor = self._font_color.to_rgb()

        # widget dictionary
        # fmt: off
        self._widget_dictionary = Dictionary()
        self._widget_dictionary.set_is_unique(True)
        self._widget_dictionary[Name("AP")] = widget_appearance_dictionary
        self._widget_dictionary[Name("AS")] = Name("Off")
        self._widget_dictionary[Name("DA")] = String(
            "%f %f %f rg /%s %f Tf"
            % (
                float(font_color_rgb.red),
                float(font_color_rgb.green),
                float(font_color_rgb.blue),
                font_resource_name,
                0,
            )
        )
        self._widget_dictionary[Name("DR")] = widget_resources
        self._widget_dictionary[Name("DV")] = Name("Off")
        self._widget_dictionary[Name("F")] = bDecimal(4)
        self._widget_dictionary[Name("FT")] = Name("Btn")
        self._widget_dictionary[Name("MK")] = Dictionary()
        self._widget_dictionary[Name("MK")][Name("CA")] = bString("8")
        self._widget_dictionary[Name("P")] = catalog
        self._widget_dictionary[Name("Rect")] = bList().set_is_inline(True)
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.x))
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.y + layout_box.height - self._font_size - 2))
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.x + layout_box.width))
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.y + layout_box.height))
        self._widget_dictionary[Name("Subtype")] = Name("Widget")
        self._widget_dictionary[Name("T")] = bString(self._field_name or self._get_auto_generated_field_name(page))
        self._widget_dictionary[Name("Type")] = Name("Annot")
        self._widget_dictionary[Name("V")] = Name("Off")
        # fmt: on

        # append field to page /Annots
        if "Annots" not in page:
            page[Name("Annots")] = bList()
        page["Annots"].append(self._widget_dictionary)

        # append field to catalog
        if "AcroForm" not in catalog:
            catalog[Name("AcroForm")] = Dictionary()
            catalog["AcroForm"][Name("DR")] = widget_resources
            catalog["AcroForm"][Name("Fields")] = bList()
            catalog["AcroForm"][Name("NeedAppearances")] = Boolean(True)
        catalog["AcroForm"]["Fields"].append(self._widget_dictionary)

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:
        # init self._widget_dictionary
        self._init_widget_dictionary(page, content_box)

        # set location
        # fmt: off
        assert self._font_size is not None
        line_height: Decimal = self._font_size * Decimal(1.2)
        if self._widget_dictionary is not None:
            self._widget_dictionary["Rect"][0] = bDecimal(content_box.get_x())
            self._widget_dictionary["Rect"][1] = bDecimal(content_box.get_y() + content_box.height - line_height)
            self._widget_dictionary["Rect"][2] = bDecimal(content_box.get_x() + content_box.width)
            self._widget_dictionary["Rect"][3] = bDecimal(content_box.get_y() + line_height)
        # fmt: on

    #
    # PUBLIC
    #
