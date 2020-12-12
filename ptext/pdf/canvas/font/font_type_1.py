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
        # self
        if "FontDescriptor" in self and "AvgWidth" in self["FontDescriptor"]:
            return self["FontDescriptor"]["AvgWidth"]
        # standard 14
        standard_14_font = AdobeFontMetrics.get(self.get_font_name())
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "AvgWidth" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["AvgWidth"]
        # default
        return None

    def get_ascent(self) -> Optional[Decimal]:
        # self
        if "FontDescriptor" in self and "Ascent" in self["FontDescriptor"]:
            return self["FontDescriptor"]["Ascent"]
        # standard 14
        standard_14_font = AdobeFontMetrics.get(self.get_font_name())
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "Ascent" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["Ascent"]
        # default
        return None

    def get_descent(self) -> Optional[Decimal]:
        # self
        if "FontDescriptor" in self and "Descent" in self["FontDescriptor"]:
            return self["FontDescriptor"]["Descent"]
        # standard 14
        standard_14_font = AdobeFontMetrics.get(self.get_font_name())
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "Descent" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["Descent"]
        # default
        return None

    def get_single_character_width(self, character_code: int) -> Optional[Decimal]:
        # self
        if "Widths" in self and "FirstChar" in self and "LastChar" in self:
            if self["FirstChar"] <= character_code <= self["LastChar"] and len(
                self["Widths"]
            ) >= (self["LastChar"] - self["FirstChar"]):
                return self["Widths"][int(character_code - self["FirstChar"])]
            return None
        # standard 14
        standard_14_font = AdobeFontMetrics.get(self.get_font_name())
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

    def get_missing_character_width(self) -> Optional[Decimal]:
        # self
        if "FontDescriptor" in self and "MissingWidth" in self["FontDescriptor"]:
            return self["FontDescriptor"]["MissingWidth"]
        # standard 14
        standard_14_font = AdobeFontMetrics.get(self.get_font_name())
        if (
            standard_14_font is not None
            and "FontDescriptor" in standard_14_font
            and "MissingWidth" in standard_14_font["FontDescriptor"]
        ):
            return standard_14_font["FontDescriptor"]["MissingWidth"]
        # default
        return None

    def get_font_name(self) -> Optional[str]:
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
