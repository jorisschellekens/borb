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

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.font.font import Font
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
            margin_top=margin_top or Decimal(0),
            margin_right=margin_right or Decimal(0),
            margin_bottom=margin_bottom or Decimal(0),
            margin_left=margin_left or Decimal(0),
            background_color=background_color,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            multiplied_leading=multiplied_leading,
            fixed_leading=fixed_leading,
        )
