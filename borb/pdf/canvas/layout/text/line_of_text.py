#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    LineOfText represents a single line of text
    LineOfText supports:
    - font
    - font_color
    - font_size
    - borders: border_top, border_right, border_bottom, border_left
    - border_color
    - border_width
    - padding: padding_top, padding_right, padding_bottom, padding_left
    - background_color
    - horizontal_alignment
    - vertical_alignment
    text_alignment is not applicable for LineOfText, as its bounding box will always be the exact width needed
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.glyph_line import GlyphLine
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class LineOfText(ChunkOfText):
    """
    LineOfText represents a single line of text
    LineOfText supports:
    - font
    - font_color
    - font_size
    - borders: border_top, border_right, border_bottom, border_left
    - border_color
    - border_width
    - padding: padding_top, padding_right, padding_bottom, padding_left
    - background_color
    - horizontal_alignment
    - vertical_alignment
    text_alignment is not applicable for LineOfText, as its bounding box will always be the exact width needed
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        font: typing.Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
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
        background_color: typing.Optional[Color] = None,
        fixed_leading: typing.Optional[Decimal] = None,
        multiplied_leading: typing.Optional[Decimal] = None,
        text_alignment: Alignment = Alignment.LEFT,
    ):
        super().__init__(
            text=text,
            font=font,
            font_size=font_size,
            font_color=font_color,
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
            margin_bottom=margin_bottom if margin_bottom is not None else Decimal(0),
            margin_left=margin_left if margin_left is not None else Decimal(0),
            margin_right=margin_right if margin_right is not None else Decimal(0),
            margin_top=margin_top if margin_top is not None else Decimal(0),
            background_color=background_color,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            multiplied_leading=multiplied_leading,
            fixed_leading=fixed_leading,
        )
        # alignment
        assert text_alignment in [
            Alignment.LEFT,
            Alignment.CENTERED,
            Alignment.RIGHT,
            Alignment.JUSTIFIED,
        ]
        self._text_alignment = text_alignment

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        # for text_alignment == JUSTIFIED we handle it ourselves
        # otherwise we delegate to super
        if self._text_alignment == Alignment.JUSTIFIED:
            # determine line height
            assert self._font_size is not None
            line_height: Decimal = self._font_size
            if self._multiplied_leading is not None:
                line_height *= self._multiplied_leading
            if self._fixed_leading is not None:
                line_height += self._fixed_leading

            # return
            return Rectangle(
                available_space.get_x(),
                available_space.get_y() + available_space.get_height() - line_height,
                available_space.get_width(),
                line_height,
            )
        else:
            return super(LineOfText, self)._get_content_box(available_space)

    def _paint_content_box(self, page: "Page", available_space: Rectangle) -> None:  # type: ignore[name-defined]
        # if the text_alignment is not JUSTIFIED, we delegate the call to our super
        if self._text_alignment != Alignment.JUSTIFIED:
            super(LineOfText, self)._paint_content_box(page, available_space)
            return

        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        # start calculating the remaining space per whitespace
        text_width: Decimal = GlyphLine.from_str(
            self._text, self._font, self._font_size
        ).get_width_in_text_space()
        remaining_space: Decimal = available_space.get_width() - text_width

        # calculate how much "extra space" we have for every whitespace character
        remaining_space_per_whitespace: Decimal = Decimal(0)
        number_of_whitespaces: int = sum([1 for x in self._text if x == " "])
        if number_of_whitespaces > 0:
            remaining_space_per_whitespace = remaining_space / number_of_whitespaces

        # build ChunkOfText objects
        chunks_of_text: typing.List[ChunkOfText] = [
            ChunkOfText(
                x + " ",
                font=self._font,
                font_size=self._font_size,
                font_color=self._font_color,
                multiplied_leading=self._multiplied_leading,
                fixed_leading=self._fixed_leading,
            )
            for x in self._text.split(" ")
        ]
        chunks_of_text[-1]._text = chunks_of_text[-1]._text[:-1]

        # paint
        prev_x: Decimal = available_space.get_x()
        for c in chunks_of_text:
            cbox: Rectangle = Rectangle(
                prev_x,
                available_space.get_y(),
                available_space.get_width(),
                line_height,
            )
            c.paint(page, cbox)
            prev_x += c._get_content_box(available_space).get_width()
            prev_x += remaining_space_per_whitespace

    #
    # PUBLIC
    #
