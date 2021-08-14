#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of FormField represents a text field.
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


class CheckBox(FormField):
    """
    This implementation of FormField represents a text field.
    """

    def __init__(
        self,
        font_size: Decimal = Decimal(12),
        font_color: Color = HexColor("000000"),
        field_name: typing.Optional[str] = None,
    ):
        super(CheckBox, self).__init__()
        assert font_size >= 0
        self._font_size = font_size
        self._font_color = font_color
        self._field_name: typing.Optional[str] = field_name

    def _do_layout(self, page: "Page", layout_box: Rectangle) -> Rectangle:

        font_resource_name: Name = self._get_font_resource_name(
            StandardType1Font("Helvetica"), page
        )

        # widget resource dictionary
        widget_resources: Dictionary = Dictionary()
        widget_resources[Name("Font")] = page["Resources"]["Font"]

        # widget "Off" appearance
        widget_off_appearance: Stream = Stream()
        widget_off_appearance[Name("Type")] = Name("XObject")
        widget_off_appearance[Name("Subtype")] = Name("Form")
        widget_off_appearance[Name("BBox")] = List().set_can_be_referenced(False)
        widget_off_appearance["BBox"].append(bDecimal(0))
        widget_off_appearance["BBox"].append(bDecimal(0))
        widget_off_appearance["BBox"].append(bDecimal(layout_box.width))
        widget_off_appearance["BBox"].append(bDecimal(self._font_size))
        bts = b"/Tx BMC EMC"
        widget_off_appearance[Name("DecodedBytes")] = bts
        widget_off_appearance[Name("Bytes")] = zlib.compress(bts, 9)
        widget_off_appearance[Name("Filter")] = Name("FlateDecode")
        widget_off_appearance[Name("Length")] = bDecimal(len(bts))

        # widget "Yes" appearance
        widget_yes_appearance: Stream = Stream()
        widget_yes_appearance[Name("Type")] = Name("XObject")
        widget_yes_appearance[Name("Subtype")] = Name("Form")
        widget_yes_appearance[Name("BBox")] = List().set_can_be_referenced(False)
        widget_yes_appearance["BBox"].append(bDecimal(0))
        widget_yes_appearance["BBox"].append(bDecimal(0))
        widget_yes_appearance["BBox"].append(bDecimal(layout_box.width))
        widget_yes_appearance["BBox"].append(bDecimal(self._font_size))
        bts = b"/Tx BMC EMC"
        widget_yes_appearance[Name("DecodedBytes")] = bts
        widget_yes_appearance[Name("Bytes")] = zlib.compress(bts, 9)
        widget_yes_appearance[Name("Filter")] = Name("FlateDecode")
        widget_yes_appearance[Name("Length")] = bDecimal(len(bts))

        # widget normal appearance
        widget_normal_appearance: Dictionary = Dictionary()
        widget_normal_appearance[Name("Off")] = widget_off_appearance
        widget_normal_appearance[Name("Yes")] = widget_yes_appearance

        # widget appearance dictionary
        widget_appearance_dictionary: Dictionary = Dictionary()
        widget_appearance_dictionary[Name("N")] = widget_normal_appearance

        # get Catalog
        catalog: Dictionary = page.get_root()["XRef"]["Trailer"]["Root"]

        widget_appearance_characteristics_dictionary: Dictionary = Dictionary()
        widget_appearance_characteristics_dictionary[Name("CA")] = String(
            "8"
        )  # clever little hack

        # widget dictionary
        widget_dictionary: Dictionary = Dictionary()
        widget_dictionary[Name("Type")] = Name("Annot")
        widget_dictionary[Name("Subtype")] = Name("Widget")
        widget_dictionary[Name("F")] = bDecimal(4)
        widget_dictionary[Name("Rect")] = List().set_can_be_referenced(False)
        widget_dictionary["Rect"].append(bDecimal(layout_box.x))
        widget_dictionary["Rect"].append(
            bDecimal(layout_box.y + layout_box.height - self._font_size - 2)
        )
        widget_dictionary["Rect"].append(bDecimal(layout_box.x + layout_box.width))
        widget_dictionary["Rect"].append(bDecimal(layout_box.y + layout_box.height))
        widget_dictionary[Name("FT")] = Name("Btn")
        widget_dictionary[Name("P")] = catalog
        widget_dictionary[
            Name("T")
        ] = self._field_name or self._get_auto_generated_field_name(page)
        widget_dictionary[Name("V")] = Name("Off")
        widget_dictionary[Name("DV")] = Name("Off")
        widget_dictionary[Name("AS")] = Name("Off")
        widget_dictionary[Name("DR")] = widget_resources
        widget_dictionary[Name("MK")] = widget_appearance_characteristics_dictionary

        font_color_rgb: RGBColor = self._font_color.to_rgb()
        widget_dictionary[Name("DA")] = String(
            "%f %f %f rg /%s %f Tf"
            % (
                font_color_rgb.red,
                font_color_rgb.green,
                font_color_rgb.blue,
                font_resource_name,
                self._font_size,
            )
        )
        widget_dictionary[Name("AP")] = widget_appearance_dictionary

        # append field to page /Annots
        if "Annots" not in page:
            page[Name("Annots")] = List()
        page["Annots"].append(widget_dictionary)

        # append field to catalog
        if "AcroForm" not in catalog:
            catalog[Name("AcroForm")] = Dictionary()
            catalog["AcroForm"][Name("Fields")] = List()
            catalog["AcroForm"][Name("DR")] = widget_resources
            catalog["AcroForm"][Name("NeedAppearances")] = Boolean(True)
        catalog["AcroForm"]["Fields"].append(widget_dictionary)

        # determine layout rectangle
        layout_rect = Rectangle(
            layout_box.x,
            layout_box.y + layout_box.height - self._font_size,
            max(layout_box.width, Decimal(64)),
            self._font_size + Decimal(10),
        )

        # return Rectangle
        return layout_rect
