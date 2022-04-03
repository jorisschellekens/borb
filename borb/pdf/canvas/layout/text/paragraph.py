#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains all the classes needed to perform layout of text-elements.
This includes; ChunkOfText, LineOfText, Paragraph and Heading
"""
import typing
from decimal import Decimal
from typing import Union

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.glyph_line import GlyphLine
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation
from borb.pdf.canvas.layout.layout_element import Alignment, LayoutElement
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.page.page import Page


class Paragraph(LineOfText):
    """
    A paragraph (from the Ancient Greek παράγραφος, parágraphos, "to write beside")
    is a self-contained unit of discourse in writing dealing with a particular point or idea.
    A paragraph consists of one or more sentences. Though not required by the syntax of any language,
    paragraphs are usually an expected part of formal writing, used to organize longer prose.
    """

    def __init__(
        self,
        text: str,
        respect_newlines_in_text: bool = False,
        respect_spaces_in_text: bool = False,
        font: Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        text_alignment: Alignment = Alignment.LEFT,
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
        fixed_leading: typing.Optional[Decimal] = None,
        multiplied_leading: typing.Optional[Decimal] = None,
        background_color: typing.Optional[Color] = None,
        hyphenation: typing.Optional[Hyphenation] = None,
    ):
        super().__init__(
            text=text,
            font=font,
            font_size=font_size,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
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
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            multiplied_leading=multiplied_leading,
            fixed_leading=fixed_leading,
            background_color=background_color,
        )
        self._respect_newlines_in_text = respect_newlines_in_text
        self._respect_spaces_in_text = respect_spaces_in_text
        self._hyphenation = hyphenation

        # alignment
        assert text_alignment in [
            Alignment.LEFT,
            Alignment.CENTERED,
            Alignment.RIGHT,
            Alignment.JUSTIFIED,
        ]
        self._text_alignment = text_alignment

    def _split_text(self, bounding_box: Rectangle) -> typing.List[str]:
        # asserts
        assert self._font_size is not None

        # attempt to split into words (preserve space if needed)
        words: typing.List[str] = [""]
        tokens_to_split_on: typing.List[str] = [" ", "\t", "\n"]

        tokens_to_preserve: typing.List[str] = []
        if self._respect_newlines_in_text:
            tokens_to_preserve.append("\n")
        if self._respect_spaces_in_text:
            tokens_to_preserve.append(" ")
            tokens_to_preserve.append("\t")

        for c in self._text:
            if c in tokens_to_split_on:
                # we have a token we split on, and preserve
                # add it to the list of words
                if c in tokens_to_preserve:
                    words.append(c)
                    words.append("")
                else:
                    # we have a token we split on, but don't preserve
                    # such as whitespace, with self.respect_spaces_in_text set to False
                    if words[-1] != "":
                        words.append("")
            else:
                # build the word that was already being built
                words[-1] += c
        words = [x for x in words if len(x) > 0]

        # build lines using words
        lines_of_text = []
        for i, w in enumerate(words):

            # split on \n
            if w == "\n" and self._respect_newlines_in_text:
                lines_of_text.append("")
                continue

            # build line of text to check if it fits the bounding box
            potential_text = lines_of_text[-1] if len(lines_of_text) > 0 else ""
            if len(potential_text) != 0 and not self._respect_spaces_in_text:
                potential_text += " "
            potential_text += w

            # check the remaining space in the box
            # checking with 0 is not a great idea due to rounding errors
            # so, as a pre-emptive measure, we round the number to 2 digits
            # fmt: off
            potential_width = GlyphLine.from_str(potential_text, self._font, self._font_size).get_width_in_text_space()
            remaining_space_in_box: Decimal = round(bounding_box.width - potential_width, 2)
            # fmt: on

            # IF there is space left over, we add the word to the lines of text being built
            if remaining_space_in_box >= Decimal(0):
                if len(lines_of_text) == 0:
                    lines_of_text.append(w)
                else:
                    if len(lines_of_text[-1]) > 0 and not self._respect_spaces_in_text:
                        lines_of_text[-1] += " "
                    lines_of_text[-1] += w

            # (ELSE) there is no more room in the box for this word,
            # BUT perhaps we can hyphenate the word
            else:
                # if no hyphenation class is provided, we can't hyphenate
                if self._hyphenation is None:
                    lines_of_text.append(w)
                    continue

                # if we have to respect the spacing in the text, we don't hyphenate
                if self._respect_spaces_in_text:
                    lines_of_text.append(w)
                    continue

                # calculate potential hyphenation breaks
                # if the word can not be broken into parts, we can't hyphenate
                hyphenated_word_parts = self._hyphenation.hyphenate(w).split(chr(173))
                if len(hyphenated_word_parts) == 1:
                    lines_of_text.append(w)
                    continue

                potential_text = lines_of_text[-1] if len(lines_of_text) > 0 else ""
                if len(potential_text) != 0 and not self._respect_spaces_in_text:
                    potential_text += " "

                # check where the text can be split, in order to fit in the bounding box
                hyphenation_split_index: int = 0
                for i in range(1, len(hyphenated_word_parts)):
                    # fmt: off
                    potential_text_after_hyphenation = potential_text + "".join([x for x in hyphenated_word_parts[0:i]]) + "-"
                    potential_width = GlyphLine.from_str(potential_text_after_hyphenation, self._font, self._font_size).get_width_in_text_space()
                    remaining_space_in_box = round(bounding_box.width - potential_width, 2)
                    # fmt: on
                    if remaining_space_in_box > Decimal(0):
                        hyphenation_split_index = i
                    else:
                        break

                # no sensible split was found
                if hyphenation_split_index == 0:
                    lines_of_text.append(w)
                    continue

                # break the text according to the hyphenation
                # fmt: off
                if len(lines_of_text[-1]) > 0 and not self._respect_spaces_in_text:
                    lines_of_text[-1] += " "
                lines_of_text[-1] += "".join([x for x in hyphenated_word_parts[0:hyphenation_split_index]]) + "-"
                lines_of_text.append("".join([x for x in hyphenated_word_parts[hyphenation_split_index:]]))
                # fmt: on

        # last-minute cleanup
        while len(lines_of_text) > 0 and lines_of_text[-1] == "":
            lines_of_text.pop(len(lines_of_text) - 1)

        # return
        return lines_of_text if len(lines_of_text) > 0 else [""]

    def _do_layout_without_padding(self, page: Page, bounding_box: Rectangle):
        # easy case
        if len(self._text) == 0:
            return Rectangle(bounding_box.x, bounding_box.y, Decimal(0), Decimal(0))

        # other easy cases
        lines_of_text = self._split_text(bounding_box)
        if len(lines_of_text) == 0:
            return Rectangle(bounding_box.x, bounding_box.y, Decimal(0), Decimal(0))

        # separate method for the harder case of Alignment.JUSTIFIED
        if self._text_alignment == Alignment.JUSTIFIED:
            return self._do_layout_without_padding_text_alignment_justified(
                lines_of_text, page, bounding_box
            )

        # delegate
        assert self._font_size is not None
        min_x: Decimal = Decimal(2048)
        min_y: Decimal = Decimal(2048)
        max_x: Decimal = Decimal(0)
        max_y: Decimal = Decimal(0)

        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        for i, l in enumerate(lines_of_text):
            r = LineOfText(
                l,
                font=self._font,
                font_size=self._font_size,
                font_color=self._font_color,
                horizontal_alignment=self._text_alignment,
                multiplied_leading=self._multiplied_leading,
                fixed_leading=self._fixed_leading,
            ).layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    bounding_box.y
                    + bounding_box.height
                    - line_height * i
                    - self._font_size,
                    bounding_box.width,
                    self._font_size,
                ),
            )
            min_x = min(r.x, min_x)
            min_y = min(r.y, min_y)
            max_x = max(r.x + r.width, max_x)
            max_y = max(r.y + r.height, max_y)
        layout_rect = Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect

    def _do_layout_without_padding_text_alignment_justified(
        self, lines_of_text: typing.List[str], page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        min_x: Decimal = Decimal(2048)
        min_y: Decimal = Decimal(2048)
        max_x: Decimal = Decimal(0)
        max_y: Decimal = Decimal(0)

        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        for i, line_of_text in enumerate(lines_of_text):

            #  When using justification,
            #  it is customary to treat the last line of a paragraph separately by simply left or right aligning it,
            #  depending on the language direction.
            if i == len(lines_of_text) - 1 and len(lines_of_text) >= 1:
                last_line_rectangle: Rectangle = LineOfText(
                    line_of_text,
                    font=self._font,
                    font_size=self._font_size,
                    font_color=self._font_color,
                    multiplied_leading=self._multiplied_leading,
                    fixed_leading=self._fixed_leading,
                ).layout(
                    page,
                    bounding_box=Rectangle(
                        bounding_box.x,
                        bounding_box.y + bounding_box.height - line_height * (i + 1),
                        bounding_box.width,
                        self._font_size,
                    ),
                )
                min_x = min(last_line_rectangle.x, min_x)
                min_y = min(last_line_rectangle.y, min_y)
                max_x = max(last_line_rectangle.x + last_line_rectangle.width, max_x)
                max_y = max(last_line_rectangle.y + last_line_rectangle.height, max_y)
                continue

            estimated_width: Decimal = GlyphLine.from_str(
                line_of_text, self._font, self._font_size
            ).get_width_in_text_space()
            remaining_space: Decimal = bounding_box.width - estimated_width

            # calculate the space that needs to be divided among the space-characters
            number_of_spaces: Decimal = Decimal(
                sum([1 for x in line_of_text if x == " "])
            )
            if number_of_spaces > 0:
                space_per_space: Decimal = remaining_space / number_of_spaces
            else:
                space_per_space = Decimal(0)
            words: typing.List[str] = line_of_text.split(" ")

            # perform layout
            x: Decimal = bounding_box.x
            for j, w in enumerate(words):
                s = w + ("" if j == len(words) - 1 else " ")
                r: Rectangle = ChunkOfText(
                    s,
                    font=self._font,
                    font_size=self._font_size,
                    font_color=self._font_color,
                    multiplied_leading=self._multiplied_leading,
                    fixed_leading=self._fixed_leading,
                ).layout(
                    page,
                    bounding_box=Rectangle(
                        x,
                        bounding_box.y + bounding_box.height - line_height * (i + 1),
                        bounding_box.width,
                        self._font_size,
                    ),
                )
                min_x = min(r.x, min_x)
                min_y = min(r.y, min_y)
                max_x = max(r.x + r.width, max_x)
                max_y = max(r.y + r.height, max_y)

                # line up our next x
                word_size = GlyphLine.from_str(
                    s, self._font, self._font_size
                ).get_width_in_text_space()
                x += word_size
                x += space_per_space

        # set bounding box
        layout_rect = Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
