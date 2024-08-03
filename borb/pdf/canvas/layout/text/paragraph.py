#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains all the classes needed to perform layout of text-elements.
This includes; ChunkOfText, LineOfText, Paragraph and Heading
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.canvas.layout.text.text_to_line_splitter import TextToLineSplitter
from borb.pdf.page.page import Page


class Paragraph(LineOfText):
    """
    A paragraph (from the Ancient Greek παράγραφος, parágraphos, "to write beside")
    is a self-contained unit of discourse in writing dealing with a particular point or idea.
    A paragraph consists of one or more sentences. Though not required by the syntax of any language,
    paragraphs are usually an expected part of formal writing, used to organize longer prose.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        fixed_leading: typing.Optional[Decimal] = None,
        font: typing.Union[Font, str] = "Helvetica",
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(12),
        horizontal_alignment: Alignment = Alignment.LEFT,
        hyphenation: typing.Optional[Hyphenation] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        multiplied_leading: typing.Optional[Decimal] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        respect_newlines_in_text: bool = False,
        respect_spaces_in_text: bool = False,
        text_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
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
        self._previous_lines_of_text: typing.Optional[typing.List[LineOfText]] = None

    #
    # PRIVATE
    #

    def __hash__(self) -> int:
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
        return attr_hash_for_layout * 69069 + 907133923

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        # This code gets screwed over by cached_by_hash
        # TODO: investigate

        # if the hash has changed, it implies some attributes that are relevant to layout have changed
        # we need to recalculate the content_box
        # otherwise we can just skip this and return the previously calculated content_box
        assert self._font_size is not None
        lines_of_text = [
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
        if self._text_alignment == Alignment.JUSTIFIED:
            lines_of_text[-1]._text_alignment = Alignment.LEFT

        # determine line height
        assert self._font_size is not None
        line_height: Decimal = self._font_size
        if self._multiplied_leading is not None:
            line_height *= self._multiplied_leading
        if self._fixed_leading is not None:
            line_height += self._fixed_leading

        # determine content box height
        h: Decimal = line_height * len(lines_of_text)

        # determine content box width
        w: Decimal = Decimal(0)
        for i, l in enumerate(lines_of_text):
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

        # store self._previous_lines_of_text
        self._previous_lines_of_text = lines_of_text

        # determine content box
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - h,
            w,
            h,
        )

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

        # check whether it can be painted
        assert self._previous_lines_of_text is not None
        if round(available_space.get_height(), 2) < round(
            line_height * len(self._previous_lines_of_text), 2
        ):
            self._split_text(available_space)
            assert False

        # call paint on all LineOfText objects
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
        return TextToLineSplitter.text_to_lines(
            bounding_box=bounding_box,
            font=self.get_font(),
            font_size=self.get_font_size(),
            text=self.get_text(),
            hyphenation=self._hyphenation,
            respect_newlines=self._respect_newlines_in_text,
            respect_spaces=self._respect_spaces_in_text,
        )

    #
    # PUBLIC
    #
