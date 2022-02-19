#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement acts as a common base class to form fields.
"""
import typing

from borb.io.read.types import Dictionary, List, Name
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class FormField(LayoutElement):
    """
    This implementation of LayoutElement acts as a common base class to form fields.
    """

    def _get_auto_generated_field_name(self, page: Page) -> str:
        number_of_fields: int = 0
        acroform_dict: Dictionary = page.get_root()["XRef"]["Trailer"]["Root"].get(  # type: ignore [attr-defined]
            "AcroForm", Dictionary()
        )
        stk: typing.List[typing.Union[Dictionary, List]] = [acroform_dict]
        exp: typing.List[int] = []
        while len(stk) > 0:
            d = stk.pop()
            if id(d) in exp:
                continue
            exp.append(id(d))
            if isinstance(d, Dictionary):
                if "Type" in d and "Subtype" in d and "FT" in d:
                    number_of_fields += 1
                for k, v in d.items():
                    if isinstance(v, Dictionary):
                        stk.append(v)
                    if isinstance(v, List):
                        stk.append(v)
            if isinstance(d, List):
                for c in d:
                    stk.append(c)
        return "field-{0:03d}".format(number_of_fields)

    def _get_font_resource_name(self, font: Font, page: Page):
        # create resources if needed
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary().set_parent(page)  # type: ignore [attr-defined]
        if "Font" not in page["Resources"]:
            page["Resources"][Name("Font")] = Dictionary()

        # insert font into resources
        font_resource_name = [
            k for k, v in page["Resources"]["Font"].items() if v == font
        ]
        if len(font_resource_name) > 0:
            return font_resource_name[0]
        else:
            font_index = len(page["Resources"]["Font"]) + 1
            page["Resources"]["Font"][Name("F%d" % font_index)] = font
            return Name("F%d" % font_index)
