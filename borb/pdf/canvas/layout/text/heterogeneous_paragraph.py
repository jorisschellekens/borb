#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents a heterogeneous Paragraph.
e.g. a Paragraph where one or more words are in bold (but not all of them)
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.emoji.emoji import Emoji
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class LineBreakChunk(ChunkOfText):
    """
    This implementation of ChunkOfText represents a linebreak.
    This can be used in the HeterogeneousParagraph to force lines to be split
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(LineBreakChunk, self).__init__(text="\n")

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #


class HeterogeneousParagraph(Paragraph):
    """
    This implementation of LayoutElement represents a heterogeneous collection of ChunkOfText elements.
    Furthermore, (like Paragraph), this element has a default top- and bottom margin.
    e.g. a Paragraph where one or more words are in bold (but not all of them)
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        chunks_of_text: typing.List[
            typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]
        ] = [],
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
        horizontal_alignment: Alignment = Alignment.LEFT,
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
        text_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(HeterogeneousParagraph, self).__init__(
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            fixed_leading=fixed_leading,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            multiplied_leading=multiplied_leading,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            respect_newlines_in_text=respect_newlines_in_text,
            text="",
            text_alignment=text_alignment,
            vertical_alignment=vertical_alignment,
        )
        # fmt: off
        self._chunks_of_text: typing.List[typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]] = chunks_of_text
        # fmt: on

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        # useful
        EMPTY_RECTANGLE: Rectangle = Rectangle(
            Decimal(0), Decimal(0), Decimal(0), Decimal(0)
        )

        # lines of text
        lines_of_text: typing.List[
            typing.List[LayoutElement]
        ] = self._split_to_lines_of_chunks_of_text(available_space)

        # determine height
        h: Decimal = Decimal(
            sum(
                [
                    max(
                        [
                            (
                                x.get_previous_layout_box() or EMPTY_RECTANGLE
                            ).get_height()
                            for x in line_of_text
                        ]
                    )
                    for line_of_text in lines_of_text
                ]
            )
        )

        # determine width
        w: Decimal = Decimal(
            max(
                [
                    sum(
                        [
                            (x.get_previous_layout_box() or EMPTY_RECTANGLE).get_width()
                            for x in line_of_text
                        ]
                    )
                    for line_of_text in lines_of_text
                ]
            )
        )
        if self._text_alignment == Alignment.JUSTIFIED:
            w = available_space.get_width()

        # return
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - h,
            w,
            h,
        )

    def _paint_content_box(self, page: Page, available_space: Rectangle) -> None:
        # lines of text
        lines_of_text: typing.List[
            typing.List[LayoutElement]
        ] = self._split_to_lines_of_chunks_of_text(available_space)

        for line in lines_of_text:
            for e in line:
                lbox: typing.Optional[Rectangle] = e.get_previous_layout_box()
                assert lbox is not None
                e.paint(page, lbox)

    def _split_to_lines_of_chunks_of_text(
        self, available_space: Rectangle
    ) -> typing.List[typing.List[LayoutElement]]:
        # useful
        EMPTY_RECTANGLE: Rectangle = Rectangle(
            Decimal(0), Decimal(0), Decimal(0), Decimal(0)
        )

        # build list
        initial_chunks_of_text: typing.List[LayoutElement] = []
        for c0 in self._chunks_of_text:
            if isinstance(c0, str):
                initial_chunks_of_text.append(
                    ChunkOfText(
                        c0,
                        border_top=self._border_top,
                        border_right=self._border_right,
                        border_bottom=self._border_bottom,
                        border_left=self._border_left,
                        border_radius_top_left=self._border_radius_top_left,
                        border_radius_top_right=self._border_radius_top_right,
                        border_radius_bottom_right=self._border_radius_bottom_right,
                        border_radius_bottom_left=self._border_radius_bottom_left,
                        background_color=self._background_color,
                        font_color=self._font_color,
                        font_size=self._font_size or Decimal(12),
                        font=self._font,
                    )
                )
                continue
            if isinstance(c0, Emoji):
                initial_chunks_of_text.append(c0)
                continue
            if isinstance(c0, Image):
                initial_chunks_of_text.append(c0)
                continue
            if isinstance(c0, ChunkOfText) and not isinstance(c0, LineOfText):
                initial_chunks_of_text.append(c0)
                continue
            if isinstance(c0, LineOfText):
                for word in c0.get_text().split(" "):
                    # TODO: continuation of borders when splitting LineOfText in ChunkOfText
                    initial_chunks_of_text.append(
                        ChunkOfText(
                            word + " ",
                            border_top=c0._border_top,
                            border_right=c0._border_right,
                            border_bottom=c0._border_bottom,
                            border_left=c0._border_left,
                            border_radius_top_left=c0._border_radius_top_left,
                            border_radius_top_right=c0._border_radius_top_right,
                            border_radius_bottom_left=c0._border_radius_bottom_left,
                            border_radius_bottom_right=c0._border_radius_bottom_right,
                            background_color=c0._background_color,
                            font_color=c0._font_color,
                            font_size=c0._font_size or Decimal(12),
                            font=c0._font,
                        )
                    )
                continue

        # perform initial layout (figure out where to break lines)
        next_x: Decimal = available_space.get_x()
        line_width: Decimal = Decimal(0)
        line: typing.List[LayoutElement] = []
        lines: typing.List[typing.List[LayoutElement]] = []
        for c1 in initial_chunks_of_text:
            w: Decimal = c1.get_layout_box(
                Rectangle(
                    next_x,
                    available_space.get_y(),
                    available_space.get_width() - line_width,
                    available_space.get_height(),
                )
            ).get_width()
            # IF the line would be too wide AND we are not respecting newlines
            # THEN split the line
            if (
                line_width + w > available_space.get_width()
            ) and not self._respect_newlines_in_text:
                # get ready for next line
                lines.append(line)
                next_x = available_space.get_x() + w
                line_width = w
                # fix the one element that does not fit
                assert c1._previous_layout_box is not None
                c1._previous_layout_box.x = available_space.get_x()
                line = [c1]
                continue
            # IF we encounter an explicit break (by means of LineBreakChunk)
            # THEN split the line
            if isinstance(c1, LineBreakChunk):
                # get ready for next line
                lines.append(line)
                next_x = available_space.get_x() + w
                line_width = w
                # fix the one element that does not fit
                assert c1._previous_layout_box is not None
                c1._previous_layout_box.x = available_space.get_x()
                line = [c1]
                continue
            # default behaviour: continue building the line
            next_x += w
            line_width += w
            line.append(c1)
        if len(line) > 0:
            lines.append(line)

        # update ys
        e_prev_layout_box: Rectangle = EMPTY_RECTANGLE
        prev_y: Decimal = available_space.get_y() + available_space.get_height()
        for line in lines:
            line_height: Decimal = max(
                [
                    (x.get_previous_layout_box() or EMPTY_RECTANGLE).get_height()
                    for x in line
                ]
            )
            y: Decimal = prev_y - line_height
            for c1 in line:
                # the next line makes the type-checker happy
                e_prev_layout_box = c1.get_previous_layout_box() or EMPTY_RECTANGLE
                delta_height: Decimal = line_height - e_prev_layout_box.get_height()
                c1.get_layout_box(
                    Rectangle(
                        e_prev_layout_box.get_x(),
                        y,
                        e_prev_layout_box.get_width(),
                        line_height - delta_height,
                    )
                )
            prev_y -= line_height

        # update xs (text_alignment == CENTERED)
        delta_x: Decimal = Decimal(0)
        line_max_x: Decimal = Decimal(0)
        cbox_max_x: Decimal = Decimal(0)
        if self._text_alignment == Alignment.CENTERED:
            for line in lines:
                line_max_x = (
                    line[-1].get_previous_layout_box() or EMPTY_RECTANGLE
                ).get_x() + (
                    line[-1].get_previous_layout_box() or EMPTY_RECTANGLE
                ).get_width()
                cbox_max_x = available_space.get_x() + available_space.get_width()
                delta_x = (cbox_max_x - line_max_x) / 2
                for c1 in line:
                    assert c1._previous_layout_box is not None
                    c1._previous_layout_box.x += delta_x

        # update xs (text_alignment == LEFT)
        if self._text_alignment == Alignment.RIGHT:
            for line in lines:
                line_max_x = (
                    line[-1].get_previous_layout_box() or EMPTY_RECTANGLE
                ).get_x() + (
                    line[-1].get_previous_layout_box() or EMPTY_RECTANGLE
                ).get_width()
                cbox_max_x = available_space.get_x() + available_space.get_width()
                delta_x = cbox_max_x - line_max_x
                for c1 in line:
                    assert c1._previous_layout_box is not None
                    c1._previous_layout_box.x += delta_x

        # update xs (text_alignment == JUSTIFIED)
        if self._text_alignment == Alignment.JUSTIFIED:
            for line in lines:
                line_max_x = (
                    line[-1].get_previous_layout_box() or EMPTY_RECTANGLE
                ).get_x() + (
                    line[-1].get_previous_layout_box() or EMPTY_RECTANGLE
                ).get_width()
                cbox_max_x = available_space.get_x() + available_space.get_width()
                delta_x = (cbox_max_x - line_max_x) / (len(line) - 1)
                for c1 in line:
                    assert c1._previous_layout_box is not None
                    c1._previous_layout_box.x += delta_x

        # return
        return lines

    #
    # PUBLIC
    #
