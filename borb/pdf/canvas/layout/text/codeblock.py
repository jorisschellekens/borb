#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In computer programming, a block or code block is a lexical structure of source code which is grouped together.
Blocks consist of one or more declarations and statements. A programming language that permits the creation of blocks,
including blocks nested within other blocks, is called a block-structured programming language.
Blocks are fundamental to structured programming, where control structures are formed from blocks.

The function of blocks in programming is to enable groups of statements to be treated as if they were one statement,
and to narrow the lexical scope of objects such as variables,
procedures and functions declared in a block so that they do not conflict with those having the same name used elsewhere.
In a block-structured programming language, the objects named in outer blocks are visible inside inner blocks,
unless they are masked by an object declared with the same name.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.paragraph import Paragraph


class CodeBlock(Paragraph):
    """
    In computer programming, a block or code block is a lexical structure of source code which is grouped together.
    Blocks consist of one or more declarations and statements. A programming language that permits the creation of blocks,
    including blocks nested within other blocks, is called a block-structured programming language.
    Blocks are fundamental to structured programming, where control structures are formed from blocks.

    The function of blocks in programming is to enable groups of statements to be treated as if they were one statement,
    and to narrow the lexical scope of objects such as variables,
    procedures and functions declared in a block so that they do not conflict with those having the same name used elsewhere.
    In a block-structured programming language, the objects named in outer blocks are visible inside inner blocks,
    unless they are masked by an object declared with the same name.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        font: typing.Union[Font, str] = "Courier",
        font_size: Decimal = Decimal(12),
        font_color: Color = HexColor("24292e"),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
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
        padding_top: Decimal = Decimal(5),
        padding_right: Decimal = Decimal(5),
        padding_bottom: Decimal = Decimal(5),
        padding_left: Decimal = Decimal(5),
        background_color: typing.Optional[Color] = HexColor("f6f8fa"),
    ):
        # format string using black
        try:
            import black  # type: ignore[import]

            text = black.format_str(text, mode=black.Mode())
        except:
            pass

        # call super
        super().__init__(
            text=text,
            font=font,
            font_size=font_size,
            font_color=font_color,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
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
            background_color=background_color,
            respect_newlines_in_text=True,
            respect_spaces_in_text=True,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
