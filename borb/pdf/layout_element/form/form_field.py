#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A tagging class representing a form field in a PDF.

This class serves as a base for different types of form fields, such as text fields, checkboxes, and dropdowns.
It inherits from LayoutElement but does not add any additional functionality on its own.
"""
import typing

from borb.pdf.font.font import Font
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name, PDFType


class FormField(LayoutElement):
    """
    A tagging class representing a form field in a PDF.

    This class serves as a base for different types of form fields, such as text fields, checkboxes, and dropdowns.
    It inherits from LayoutElement but does not add any additional functionality on its own.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __cmp_font_dictionaries(f0: Font, f1: Font) -> bool:
        for key in f0.keys() | f1.keys():
            if key == "Name":
                continue
            if f0.get(key, None) != f1.get(key, None):
                return False
        return True

    def __get_auto_generated_field_name(self, page: Page) -> str:
        document = page.get_document()
        assert document is not None
        number_of_fields: int = len(
            document.get("Trailer", {})
            .get("Root", {})
            .get("AcroForm", {})
            .get("Fields", [])
        )
        return f"field-{number_of_fields:03d}"

    def __get_font_resource_name(self, font: Font, page: Page):

        document = page.get_document()
        catalog: typing.Dict[str, PDFType] = document["Trailer"]["Root"]  # type: ignore[attr-defined, index]
        if "AcroForm" not in catalog:
            catalog[name("AcroForm")] = {
                name("Fields"): [],
                name("DR"): {name("Font"): {}},
                name("NeedAppearances"): True,
            }
        acroform: typing.Dict[typing.Union[name, str], PDFType] = catalog["AcroForm"]  # type: ignore[assignment, index, operator]
        if "DR" not in acroform:
            acroform[name("DR")] = {}
        if "Font" not in acroform["DR"]:  # type: ignore[operator]
            acroform["DR"][name("Font")] = {}  # type: ignore[call-overload, index]

        # IF the font is already present
        # THEN return that particular font
        font_name: typing.Optional[str] = next(
            iter(
                [
                    k
                    for k, v in acroform["DR"]["Font"].items()  # type: ignore[union-attr, index, call-overload]
                    if FormField.__cmp_font_dictionaries(v, font)  # type: ignore[arg-type]
                ]
            ),
            None,
        )
        if font_name is not None:
            return font_name

        # IF the font is not yet present
        # THEN create it
        if font_name is None:
            font_name = "F1"
            while font_name in acroform["DR"]["Font"].keys():  # type: ignore[union-attr, index, call-overload]
                font_name = f"F{int(font_name[1:]) + 1}"
            assert font_name is not None
            font["Name"] = name(font_name)
            acroform["DR"]["Font"][name(font_name)] = font  # type: ignore[index, call-overload]

        # return
        return name(font_name)

    #
    # PUBLIC
    #

    pass
