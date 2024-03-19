#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents one uninterrupted block of text
"""
import typing
from decimal import Decimal

from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.glyph_line import GlyphLine
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class ChunkOfText(LayoutElement):
    """
    This implementation of LayoutElement represents one uninterrupted block of text
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        font: typing.Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        font_color: Color = HexColor("000000"),
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_bottom_left: Decimal = Decimal(0),
        border_color: Color = HexColor("000000"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        margin_top: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
        fixed_leading: typing.Optional[Decimal] = None,
        multiplied_leading: typing.Optional[Decimal] = None,
        background_color: typing.Optional[Color] = None,
    ):
        super().__init__(
            font_size=font_size,
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_bottom_left=border_radius_bottom_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            margin_top=margin_top or Decimal(0),
            margin_right=margin_right or Decimal(0),
            margin_bottom=margin_bottom or Decimal(0),
            margin_left=margin_left or Decimal(0),
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            background_color=background_color,
        )
        self._text: str = text
        self._is_tagged: bool = False

        # font information
        if isinstance(font, str):
            self._font: Font = StandardType1Font(font)
            assert self._font
        else:
            self._font = font
        self._font_color = font_color

        # leading
        if fixed_leading is None and multiplied_leading is None:
            multiplied_leading = Decimal(1.2)
        assert fixed_leading is not None or multiplied_leading is not None
        assert fixed_leading is None or fixed_leading > 0
        assert multiplied_leading is None or multiplied_leading > 0
        self._multiplied_leading: typing.Optional[Decimal] = multiplied_leading
        self._fixed_leading: typing.Optional[Decimal] = fixed_leading

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        # line height
        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        # width
        w: Decimal = GlyphLine.from_str(
            self._text, self._font, self._font_size
        ).get_width_in_text_space()

        # return
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - line_height,
            w,
            line_height,
        )

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

    def _pad_string_with_zeroes(self, s: str, n: int = 2) -> str:
        while len(s) < n:
            s = "0" + s
        return s

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:
        # color
        assert self._font is not None
        rgb_color = self._font_color.to_rgb()

        # line height
        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        # descent
        # TODO
        descent: Decimal = (self._font.get_descent() / Decimal(1000)) * self._font_size

        # determine what to write to page
        content = """q\nBT\n%f %f %f rg\n/%s %f Tf\n%f 0 0 %f %f %f Tm\n%s\nET\nQ""" % (
            float(rgb_color.red),  # rg
            float(rgb_color.green),  # rg
            float(rgb_color.blue),  # rg
            self._get_font_resource_name(self._font, page),  # Tf
            float(1),  # Tf
            float(self._font_size),  # Tm
            float(self._font_size),  # Tm
            float(content_box.get_x()),  # Tm
            float(
                content_box.get_y()
                + content_box.get_height()
                - self._font_size
                - descent
            ),  # Tm
            self._write_text_bytes(),  # Tj
        )
        page.append_to_content_stream(content)

    def _write_text_bytes(self) -> str:
        hex_mode: bool = False
        # check glyphs
        for c in self._text:
            if ord(c) != self._font.unicode_to_character_identifier(c):
                hex_mode = True
                break
        # delegate
        if hex_mode or isinstance(self._font, TrueTypeFont):
            return self._write_text_bytes_in_hex()
        else:
            return self._write_text_bytes_in_ascii()

    def _write_text_bytes_in_ascii(self) -> str:
        """
        This function escapes certain reserved characters in PDF strings.
        """
        sOut: str = ""
        for c in self._text:
            if c == "\r":
                sOut += "\\r"
            elif c == "\n":
                sOut += "\\n"
            elif c == "\t":
                sOut += "\\t"
            elif c == "\b":
                sOut += "\\b"
            elif c == "\f":
                sOut += "\\f"
            elif c in ["(", ")", "\\"]:
                sOut += "\\" + c
            elif 0 <= ord(c) < 8:
                sOut += "\\00" + oct(ord(c))[2:]
            elif 8 <= ord(c) < 32:
                sOut += "\\0" + oct(ord(c))[2:]
            else:
                sOut += c
        # default
        return "".join(["(", sOut, ") Tj"])

    def _write_text_bytes_in_hex(self) -> str:
        # decide whether we should write 1 byte, or 2 bytes
        font: Font = self._font
        use_four_bytes: bool = False
        if "Encoding" in font and font["Encoding"] in ["Identity-H", "Identity-V"]:
            use_four_bytes = True

        # write each cid
        sOut: str = ""
        for c in self._text:
            cid: typing.Optional[int] = self._font.unicode_to_character_identifier(c)
            assert cid is not None, "Font %s can not represent '%s'" % (
                self._font.get_font_name(),
                c,
            )
            hex_rep: str = hex(int(cid))[2:]
            hex_rep = self._pad_string_with_zeroes(hex_rep, 4 if use_four_bytes else 2)
            sOut += "".join(["<", hex_rep, ">"])
        return "".join(["[", sOut, "] TJ"])

    #
    # PUBLIC
    #

    def get_font(self) -> Font:
        """
        This function returns the Font of this LayoutElement
        :return:    the Font
        """
        return self._font

    def get_font_color(self) -> Color:
        """
        This function returns the font Color of this LayoutElement
        :return:    the font Color
        """
        return self._font_color

    def get_text(self) -> str:
        """
        This function returns the text of this LayoutElement
        :return:    the text
        """
        return self._text
