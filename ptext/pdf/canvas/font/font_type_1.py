# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A Type 1 font program is a stylized PostScript program that describes glyph shapes. It uses a compact
    encoding for the glyph descriptions, and it includes hint information that enables high-quality rendering even at
    small sizes and low resolutions.
"""
import copy
from decimal import Decimal
from typing import Optional

from ptext.pdf.canvas.font.afm.adobe_font_metrics import AdobeFontMetrics
from ptext.pdf.canvas.font.font import Font


class FontType1(Font):
    """
    A Type 1 font program is a stylized PostScript program that describes glyph shapes. It uses a compact
    encoding for the glyph descriptions, and it includes hint information that enables high-quality rendering even at
    small sizes and low resolutions.
    """

    def get_average_character_width(self) -> Optional[Decimal]:
        """
        (Optional) The average width of glyphs in the font. Default value: 0.
        """

        # self
        if "FontDescriptor" in self and "AvgWidth" in self["FontDescriptor"]:
            return self["FontDescriptor"]["AvgWidth"]

        # standard 14
        font_name: Optional[str] = self.get_font_name()
        assert font_name is not None
        standard_14_font = AdobeFontMetrics.get(font_name)
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "AvgWidth" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["AvgWidth"]

        # default
        return None

    def get_ascent(self) -> Optional[Decimal]:
        """
        (Required, except for Type 3 fonts) The maximum height above the
        baseline reached by glyphs in this font. The height of glyphs for
        accented characters shall be excluded.
        """

        # self
        if "FontDescriptor" in self and "Ascent" in self["FontDescriptor"]:
            return self["FontDescriptor"]["Ascent"]

        # standard 14
        font_name: Optional[str] = self.get_font_name()
        assert font_name is not None
        standard_14_font = AdobeFontMetrics.get(font_name)
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "Ascent" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["Ascent"]

        # default
        return None

    def get_descent(self) -> Optional[Decimal]:
        """
        (Required, except for Type 3 fonts) The maximum depth below the
        baseline reached by glyphs in this font. The value shall be a negative
        number.
        """
        # self
        if "FontDescriptor" in self and "Descent" in self["FontDescriptor"]:
            return self["FontDescriptor"]["Descent"]
        # standard 14
        font_name: Optional[str] = self.get_font_name()
        assert font_name is not None
        standard_14_font = AdobeFontMetrics.get(font_name)
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "Descent" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["Descent"]
        # default
        return None

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        """
        Get the width (in text space) of a given character code.
        Returns None if the character code can not be represented in this Font.
        """

        # self
        if "Widths" in self and "FirstChar" in self and "LastChar" in self:
            if self["FirstChar"] <= character_code <= self["LastChar"] and len(
                self["Widths"]
            ) >= (self["LastChar"] - self["FirstChar"]):
                return self["Widths"][int(character_code - self["FirstChar"])]
            return None

        # standard 14
        font_name: Optional[str] = self.get_font_name()
        assert font_name is not None
        standard_14_font = AdobeFontMetrics.get(font_name)
        if (
            standard_14_font is not None
            and "Widths" in standard_14_font
            and "FirstChar" in standard_14_font
            and "LastChar" in standard_14_font
        ):
            if standard_14_font["FirstChar"] <= character_code <= standard_14_font[
                "LastChar"
            ] and len(standard_14_font["Widths"]) >= (
                standard_14_font["LastChar"] - standard_14_font["FirstChar"]
            ):
                return standard_14_font["Widths"][
                    int(character_code - standard_14_font["FirstChar"])
                ]

        # default
        return None

    def get_missing_character_width(self) -> Decimal:
        """
        (Optional) The width to use for character codes whose widths are not
        specified in a font dictionary’s Widths array. This shall have a
        predictable effect only if all such codes map to glyphs whose actual
        widths are the same as the value of the MissingWidth entry. Default
        value: 0.
        """
        # self
        if "FontDescriptor" in self and "MissingWidth" in self["FontDescriptor"]:
            return self["FontDescriptor"]["MissingWidth"]
        # standard 14
        font_name: Optional[str] = self.get_font_name()
        assert font_name is not None
        standard_14_font = AdobeFontMetrics.get(font_name)
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "MissingWidth" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["MissingWidth"]
        # default
        return Decimal(250)

    def get_font_name(self) -> Optional[str]:
        """
        (Required) The PostScript name of the font. For Type 1 fonts, this is
        always the value of the FontName entry in the font program; for more
        information, see Section 5.2 of the PostScript Language Reference,
        Third Edition. The PostScript name of the font may be used to find the
        font program in the conforming reader or its environment. It is also the
        name that is used when printing to a PostScript output device.
        """
        return self.get("BaseFont") or self.get("Name")

    def __deepcopy__(self, memodict={}):
        copy_out = FontType1()
        for k in ["Type", "Subtype", "BaseFont"]:
            copy_out[k] = self[k]
        for k in ["Name", "FirstChar", "LastChar"]:
            if k in self:
                copy_out[k] = self.get(k)
        for k in ["Widths", "FontDescriptor", "Encoding", "ToUnicode"]:
            if k in self:
                copy_out[k] = copy.deepcopy(self.get(k), memodict)
        # return
        return copy_out
