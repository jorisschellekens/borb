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
from borb.pdf.canvas.layout.layout_element import Alignment
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

        # layout
        self._previous_content_box: typing.Optional[Rectangle] = None
        self._previous_attr_hash_for_layout: typing.Optional[int] = None
        self._previous_lines_of_text: typing.Optional[typing.List[LineOfText]] = None

    def _calculate_attribute_hash_for_content_box(self) -> int:
        attr: typing.List[typing.Any] = [
            self._text,
            self._font,
            self._font_size,
            self._vertical_alignment,
            self._horizontal_alignment,
            self._font_color,
            self._border_top,
            self._border_right,
            self._border_bottom,
            self._border_left,
            self._border_radius_top_left,
            self._border_radius_top_right,
            self._border_radius_bottom_right,
            self._border_radius_bottom_left,
            self._border_color,
            self._border_width,
            self._padding_top,
            self._padding_right,
            self._padding_bottom,
            self._padding_left,
            self._margin_top,
            self._margin_right,
            self._margin_bottom,
            self._margin_left,
            self._multiplied_leading,
            self._fixed_leading,
            self._background_color,
        ]
        attr_hash_for_layout: int = 1927868237
        for a in attr:
            h: int = hash(a)
            attr_hash_for_layout ^= (h ^ (h << 16) ^ 89869747) * 3644798167
        attr_hash_for_layout = attr_hash_for_layout * 69069 + 907133923

        # return
        return attr_hash_for_layout

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:

        # compare hash
        attr_hash_for_layout: int = self._calculate_attribute_hash_for_content_box()

        # check whether we are calculating the available space
        # using the same (Paragraph) attributes using a previous content box
        # if so, return the previous content_box
        # if this Paragraph previously fit in that box, and nothing has changed (e.g. font_size, leading, etc)
        # then this Paragraph still fits inside that box
        if (
            self._previous_content_box is not None
            and available_space == self._previous_content_box
            and attr_hash_for_layout == self._previous_attr_hash_for_layout
        ):
            return self._previous_content_box

        # if the hash has changed, it implies some attributes that are relevant to layout have changed
        # we need to recalculate the content_box
        # otherwise we can just skip this and return the previously calculated content_box
        assert self._font_size is not None
        self._previous_attr_hash_for_layout = attr_hash_for_layout
        self._previous_lines_of_text = [
            LineOfText(
                x,
                font=self._font,
                font_size=self._font_size,
                font_color=self._font_color,
                horizontal_alignment=self._text_alignment,
                multiplied_leading=self._multiplied_leading,
                text_alignment=self._text_alignment,
                fixed_leading=self._fixed_leading,
            )
            for x in self._split_text(available_space)
        ]

        #  When using justification,
        #  it is customary to treat the last line of a paragraph separately by simply left or right aligning it,
        #  depending on the language direction.
        if (
            self._text_alignment == Alignment.JUSTIFIED
            and len(self._previous_lines_of_text) > 1
        ):
            self._previous_lines_of_text[-1]._text_alignment = Alignment.LEFT

        # determine line height
        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        # determine content box height
        h: Decimal = line_height * len(self._previous_lines_of_text)

        # determine content box width
        w: Decimal = Decimal(0)
        for i, l in enumerate(self._previous_lines_of_text):
            lbox: Rectangle = l._get_content_box(
                Rectangle(
                    available_space.get_x(),
                    available_space.get_y()
                    + available_space.get_height()
                    - (i + 1) * line_height,
                    available_space.get_width(),
                    line_height,
                )
            )
            w = max(w, lbox.get_width())

        # determine content box
        self._previous_content_box = Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - h,
            w,
            h,
        )

        # return
        return self._previous_content_box

    def _paint_content_box(self, page: Page, available_space: Rectangle) -> None:

        # ensure everything is initialized
        self._get_content_box(available_space)

        # determine line height
        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        # if the Paragraph needs to be tagged, insert (STARTING) tagging operators
        # TODO: determine next MCID
        if self._needs_to_be_tagged(page):
            next_mcid: int = 0
            page.append_to_content_stream("\n/Standard <</MCID %d>>\nBDC\n" % next_mcid)

        # call paint on all LineOfText objects
        assert self._previous_lines_of_text is not None
        for i, l in enumerate(self._previous_lines_of_text):
            l.paint(
                page,
                Rectangle(
                    available_space.get_x(),
                    available_space.get_y()
                    + available_space.get_height()
                    - (i + 1) * line_height,
                    available_space.get_width(),
                    line_height,
                ),
            )

        # if the Paragraph needs to be tagged, insert (CLOSING) tagging operators
        if self._needs_to_be_tagged(page):
            page.append_to_content_stream("\nEMC\n")

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

                # fmt: off
                # break the text according to the hyphenation
                # IF there is a previous line of text, we can append it to that line
                if len(lines_of_text) > 0:
                    if len(lines_of_text[-1]) > 0 and not self._respect_spaces_in_text:
                        lines_of_text[-1] += " "
                    lines_of_text[-1] += "".join([x for x in hyphenated_word_parts[0:hyphenation_split_index]]) + "-"
                # ELSE the hyphenated word is added (in parts) to lines_of_text
                else:
                    lines_of_text.append("".join([x for x in hyphenated_word_parts[0:hyphenation_split_index]]) + "-")
                lines_of_text.append("".join([x for x in hyphenated_word_parts[hyphenation_split_index:]]))
                # fmt: on

        # last-minute cleanup
        while len(lines_of_text) > 0 and lines_of_text[-1] == "":
            lines_of_text.pop(len(lines_of_text) - 1)

        # return
        return lines_of_text if len(lines_of_text) > 0 else [""]
