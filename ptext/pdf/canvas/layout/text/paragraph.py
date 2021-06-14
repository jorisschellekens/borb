#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file contains all the classes needed to perform layout of text-elements.
    This includes; ChunkOfText, LineOfText, Paragraph and Heading
"""
import typing
from decimal import Decimal
from typing import Union

from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.glyph_line import GlyphLine
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.layout_element import Alignment, LayoutElement
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.canvas.layout.text.line_of_text import LineOfText
from ptext.pdf.page.page import Page


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
        font_color: Color = X11Color("Black"),
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,
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
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            background_color=background_color,
            parent=parent,
        )
        self.respect_newlines_in_text = respect_newlines_in_text
        self.respect_spaces_in_text = respect_spaces_in_text
        assert text_alignment in [
            Alignment.LEFT,
            Alignment.CENTERED,
            Alignment.RIGHT,
            Alignment.JUSTIFIED,
        ]
        self.text_alignment = text_alignment

    def _split_text(self, bounding_box: Rectangle) -> typing.List[str]:
        # attempt to split into words (preserve space if needed)
        words: typing.List[str] = [""]
        tokens_to_split_on: typing.List[str] = [" ", "\t", "\n"]

        tokens_to_preserve: typing.List[str] = []
        if self.respect_newlines_in_text:
            tokens_to_preserve.append("\n")
        if self.respect_spaces_in_text:
            tokens_to_preserve.append(" ")
            tokens_to_preserve.append("\t")

        for c in self.text:
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
            if w == "\n" and self.respect_newlines_in_text:
                lines_of_text.append("")
                continue

            # build line of text to check if it fits the bounding box
            potential_text = lines_of_text[-1] if len(lines_of_text) > 0 else ""
            if len(potential_text) != 0 and not self.respect_spaces_in_text:
                potential_text += " "
            potential_text += w

            # check the width of this piece of text
            encoded_bytes: bytes = bytes(
                [
                    self.font.unicode_to_character_identifier(c) or 0
                    for c in potential_text
                ]
            )
            potential_width = GlyphLine(
                encoded_bytes, self.font, self.font_size
            ).get_width_in_text_space()

            # if this text is larger than the bounding box, split the text
            remaining_space_in_box: Decimal = bounding_box.width - potential_width
            if remaining_space_in_box > Decimal(
                -1
            ):  # checking with 0 is not a great idea due to rounding errors
                if len(lines_of_text) == 0:
                    lines_of_text.append(w)
                else:
                    if len(lines_of_text[-1]) > 0 and not self.respect_spaces_in_text:
                        lines_of_text[-1] += " "
                    lines_of_text[-1] += w
            else:
                lines_of_text.append(w)

        while len(lines_of_text) > 0 and lines_of_text[-1] == "":
            lines_of_text.pop(len(lines_of_text) - 1)

        # return
        return lines_of_text if len(lines_of_text) > 0 else [""]

    def _do_layout_without_padding(self, page: Page, bounding_box: Rectangle):
        # easy case
        if len(self.text) == 0:
            return Rectangle(bounding_box.x, bounding_box.y, Decimal(0), Decimal(0))

        # other easy cases
        lines_of_text = self._split_text(bounding_box)
        if len(lines_of_text) == 0:
            return Rectangle(bounding_box.x, bounding_box.y, Decimal(0), Decimal(0))

        # separate method for the harder case of Alignment.JUSTIFIED
        if self.text_alignment == Alignment.JUSTIFIED:
            return self._do_layout_without_padding_text_alignment_justified(
                lines_of_text, page, bounding_box
            )

        # delegate
        min_x: Decimal = Decimal(2048)
        min_y: Decimal = Decimal(2048)
        max_x: Decimal = Decimal(0)
        max_y: Decimal = Decimal(0)
        leading: Decimal = self.font_size * Decimal(1.3)
        for i, l in enumerate(lines_of_text):
            r = LineOfText(
                l,
                font=self.font,
                font_size=self.font_size,
                font_color=self.font_color,
                horizontal_alignment=self.text_alignment,
                parent=self,
            ).layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    bounding_box.y + bounding_box.height - leading * i - self.font_size,
                    bounding_box.width,
                    self.font_size,
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
        leading: Decimal = self.font_size * Decimal(1.3)

        for i, line_of_text in enumerate(lines_of_text):

            #  When using justification,
            #  it is customary to treat the last line of a paragraph separately by simply left or right aligning it,
            #  depending on the language direction.
            if i == len(lines_of_text) - 1 and len(lines_of_text) > 1:
                last_line_rectangle: Rectangle = LineOfText(
                    line_of_text,
                    font=self.font,
                    font_size=self.font_size,
                    font_color=self.font_color,
                    parent=self,
                ).layout(
                    page,
                    bounding_box=Rectangle(
                        bounding_box.x,
                        bounding_box.y
                        + bounding_box.height
                        - leading * i
                        - self.font_size,
                        bounding_box.width,
                        self.font_size,
                    ),
                )
                min_x = min(last_line_rectangle.x, min_x)
                min_y = min(last_line_rectangle.y, min_y)
                max_x = max(last_line_rectangle.x + last_line_rectangle.width, max_x)
                max_y = max(last_line_rectangle.y + last_line_rectangle.height, max_y)
                continue

            encoded_bytes: bytes = bytes(
                [
                    self.font.unicode_to_character_identifier(c) or 0
                    for c in line_of_text
                ]
            )
            estimated_width: Decimal = GlyphLine(
                encoded_bytes, self.font, self.font_size
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
            for w in words:
                s = w + " "
                r: Rectangle = ChunkOfText(
                    s,
                    font=self.font,
                    font_size=self.font_size,
                    font_color=self.font_color,
                    parent=self,
                ).layout(
                    page,
                    bounding_box=Rectangle(
                        x,
                        bounding_box.y
                        + bounding_box.height
                        - leading * i
                        - self.font_size,
                        bounding_box.width,
                        self.font_size,
                    ),
                )
                min_x = min(r.x, min_x)
                min_y = min(r.y, min_y)
                max_x = max(r.x + r.width, max_x)
                max_y = max(r.y + r.height, max_y)

                # line up our next x
                encoded_bytes = bytes(
                    [self.font.unicode_to_character_identifier(c) or 0 for c in s]
                )
                word_size = GlyphLine(
                    encoded_bytes, self.font, self.font_size
                ).get_width_in_text_space()
                x += word_size
                x += space_per_space

        # set bounding box
        layout_rect = Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
