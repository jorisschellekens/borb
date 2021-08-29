#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of FormField represents a drop down list.
"""
import zlib

import typing

from borb.io.read.types import (
    Dictionary,
    Name,
    Decimal,
    List,
    String,
    Stream,
    Boolean,
)
from borb.io.read.types import Decimal as bDecimal
from borb.pdf.canvas.color.color import Color, HexColor, RGBColor
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.forms.form_field import FormField
from borb.pdf.page.page import Page


class DropDownList(FormField):
    """
    This implementation of FormField represents a drop down list.
    """

    def __init__(
        self,
        possible_values: typing.List[str],
        font_size: Decimal = Decimal(12),
        font_color: Color = HexColor("000000"),
        value: str = "",
        default_value: str = "",
        field_name: typing.Optional[str] = None,
    ):
        super(DropDownList, self).__init__()
        assert font_size >= 0
        self._font_size = font_size
        self._font_color = font_color
        self._value: str = value
        self._possible_values: typing.List[str] = possible_values
        self._default_value: str = default_value
        self._field_name: typing.Optional[str] = field_name
        self._widget_dictionary: typing.Optional[Dictionary] = None

    def _init_widget_dictionary(self, page: Page, layout_box: Rectangle) -> None:

        if self._widget_dictionary is not None:
            return

        # init page and font resources
        assert self._font_size is not None
        font_resource_name: Name = self._get_font_resource_name(
            StandardType1Font("Helvetica"), page
        )

        # widget resource dictionary
        widget_resources: Dictionary = Dictionary()
        widget_resources[Name("Font")] = page["Resources"]["Font"]

        # widget normal appearance
        widget_normal_appearance: Stream = Stream()
        widget_normal_appearance[Name("Type")] = Name("XObject")
        widget_normal_appearance[Name("Subtype")] = Name("Form")
        widget_normal_appearance[Name("BBox")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        widget_normal_appearance["BBox"].append(bDecimal(0))
        widget_normal_appearance["BBox"].append(bDecimal(0))
        widget_normal_appearance["BBox"].append(bDecimal(layout_box.width))
        widget_normal_appearance["BBox"].append(bDecimal(self._font_size))
        widget_normal_appearance[Name("Resources")] = widget_resources
        bts = bytes(
            "1 1 1 rg 0 0 %f %f re f* /Tx BMC EMC"
            % (layout_box.width, self._font_size),
            "latin1",
        )
        widget_normal_appearance[Name("DecodedBytes")] = bts
        widget_normal_appearance[Name("Bytes")] = zlib.compress(bts, 9)
        widget_normal_appearance[Name("Filter")] = Name("FlateDecode")
        widget_normal_appearance[Name("Length")] = bDecimal(len(bts))

        # widget appearance dictionary
        widget_appearance_dictionary: Dictionary = Dictionary()
        widget_appearance_dictionary[Name("N")] = widget_normal_appearance

        # get Catalog
        catalog: Dictionary = page.get_root()["XRef"]["Trailer"]["Root"]  # type: ignore [attr-defined]

        # widget dictionary
        self._widget_dictionary = Dictionary()
        self._widget_dictionary[Name("Type")] = Name("Annot")
        self._widget_dictionary[Name("Subtype")] = Name("Widget")
        self._widget_dictionary[Name("F")] = bDecimal(4)
        self._widget_dictionary[Name("Rect")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        self._widget_dictionary["Rect"].append(bDecimal(layout_box.x))
        self._widget_dictionary["Rect"].append(
            bDecimal(layout_box.y + layout_box.height - self._font_size - 2)
        )
        self._widget_dictionary["Rect"].append(
            bDecimal(layout_box.x + layout_box.width)
        )
        self._widget_dictionary["Rect"].append(
            bDecimal(layout_box.y + layout_box.height)
        )
        self._widget_dictionary[Name("FT")] = Name("Ch")
        self._widget_dictionary[Name("P")] = catalog
        self._widget_dictionary[Name("Opt")] = List()
        for x in self._possible_values:
            self._widget_dictionary["Opt"].append(String(x))
        self._widget_dictionary[Name("Ff")] = bDecimal(131072)
        self._widget_dictionary[Name("T")] = String(
            self._field_name or self._get_auto_generated_field_name(page)
        )
        self._widget_dictionary[Name("V")] = String(self._value)
        self._widget_dictionary[Name("DV")] = String(self._default_value)
        self._widget_dictionary[Name("DR")] = widget_resources

        # rendering instructions
        font_color_rgb: RGBColor = self._font_color.to_rgb()
        self._widget_dictionary[Name("DA")] = String(
            "%f %f %f rg /%s %f Tf"
            % (
                font_color_rgb.red,
                font_color_rgb.green,
                font_color_rgb.blue,
                font_resource_name,
                self._font_size,
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

    def _do_layout(self, page: "Page", layout_box: Rectangle) -> Rectangle:

        # determine layout rectangle
        assert self._font_size is not None
        layout_rect = Rectangle(
            layout_box.x,
            layout_box.y + layout_box.height - self._font_size,
            max(layout_box.width, Decimal(64)),
            self._font_size + Decimal(10),
        )

        # init self._widget_dictionary
        self._init_widget_dictionary(page, layout_rect)

        # set location
        assert self._widget_dictionary is not None
        self._widget_dictionary["AP"]["N"]["BBox"][2] = bDecimal(layout_box.width)
        self._widget_dictionary["AP"]["N"]["BBox"][3] = bDecimal(self._font_size)
        self._widget_dictionary["Rect"][0] = bDecimal(layout_box.x)
        self._widget_dictionary["Rect"][1] = bDecimal(
            layout_box.y + layout_box.height - self._font_size
        )
        self._widget_dictionary["Rect"][2] = bDecimal(layout_box.x + layout_box.width)
        self._widget_dictionary["Rect"][3] = bDecimal(layout_box.y + layout_box.height)

        # return Rectangle
        return layout_rect
