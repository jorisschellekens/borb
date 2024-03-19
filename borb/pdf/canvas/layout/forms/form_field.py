#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement acts as a common base class to form fields.
"""
import typing

from borb.io.read.pdf_object import PDFObject
from borb.io.read.types import Dictionary
from borb.io.read.types import List as bList
from borb.io.read.types import Name
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class FormField(LayoutElement):
    """
    This implementation of LayoutElement acts as a common base class to form fields.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _count_fields_on_page(self, page: Page) -> int:
        number_of_fields: int = 0

        root: typing.Optional[PDFObject] = page.get_root()
        assert root is not None
        assert isinstance(root, Dictionary)
        assert "XRef" in root

        acroform_dict: Dictionary = root["XRef"]["Trailer"]["Root"].get(
            "AcroForm", Dictionary()
        )
        stk: typing.List[typing.Union[Dictionary, bList]] = [acroform_dict]
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
                    if isinstance(v, bList):
                        stk.append(v)
            if isinstance(d, bList):
                for c in d:
                    stk.append(c)
        return number_of_fields

    def _get_auto_generated_field_name(self, page: Page) -> str:
        return "field-{0:03d}".format(self._count_fields_on_page(page))

    def _get_font_resource_name(self, font: Font, page: Page):
        # create resources if needed
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary().set_parent(page)
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

    #
    # PUBLIC
    #
