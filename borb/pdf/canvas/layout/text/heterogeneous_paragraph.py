#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents a heterogeneous Paragraph.
e.g. a Paragraph where one or more words are in bold (but not all of them)
"""
import copy
import typing
from decimal import Decimal

from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.emoji.emoji import Emoji
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class LineBreakChunk(ChunkOfText):
    """
    This implementation of ChunkOfText represents a linebreak.
    This can be used in the HeterogeneousParagraph to force lines to be split
    """

    def __init__(self):
        super(LineBreakChunk, self).__init__(text="\n")


class HeterogeneousParagraph(Paragraph):
    """
    This implementation of LayoutElement represents a heterogeneous collection of ChunkOfText elements.
    Furthermore (like Paragraph), this element has a default top- and bottom margin.
    e.g. a Paragraph where one or more words are in bold (but not all of them)
    """

    def __init__(
        self,
        chunks_of_text: typing.List[
            typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]
        ] = [],
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
        text_alignment: Alignment = Alignment.LEFT,
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
    ):
        super(HeterogeneousParagraph, self).__init__(
            text="",
            text_alignment=text_alignment,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
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
            fixed_leading=fixed_leading,
            multiplied_leading=multiplied_leading,
            background_color=background_color,
        )
        # fmt: off
        self._chunks_of_text: typing.List[typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]] = chunks_of_text
        # fmt: on

    def _split_to_lines_of_chunks_of_text(
        self, available_space: Rectangle
    ) -> typing.List[typing.List[typing.Union[ChunkOfText, Emoji, Image]]]:

        # build list
        initial_chunks_of_text: typing.List[
            typing.Union[ChunkOfText, Emoji, Image]
        ] = []
        for e in self._chunks_of_text:
            if isinstance(e, str):
                initial_chunks_of_text.append(
                    ChunkOfText(
                        e,
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
            if isinstance(e, Emoji):
                initial_chunks_of_text.append(e)
                continue
            if isinstance(e, Image):
                initial_chunks_of_text.append(e)
                continue
            if isinstance(e, LineOfText):
                for word in e.get_text().split(" "):
                    # TODO: continuation of borders when splitting LineOfText in ChunkOfText
                    initial_chunks_of_text.append(
                        ChunkOfText(
                            word + " ",
                            border_top=e._border_top,
                            border_right=e._border_right,
                            border_bottom=e._border_bottom,
                            border_left=e._border_left,
                            border_radius_top_left=e._border_radius_top_left,
                            border_radius_top_right=e._border_radius_top_right,
                            border_radius_bottom_left=e._border_radius_bottom_left,
                            border_radius_bottom_right=e._border_radius_bottom_right,
                            background_color=e._background_color,
                            font_color=e._font_color,
                            font_size=e._font_size or Decimal(12),
                            font=e._font,
                        )
                    )
                continue
            if isinstance(e, ChunkOfText):
                initial_chunks_of_text.append(e)

        # perform initial layout (figure out where to break lines)
        next_x: Decimal = available_space.get_x()
        line_width: Decimal = Decimal(0)
        line: typing.List[typing.Union[ChunkOfText, Emoji, Image]] = []
        lines: typing.List[typing.List[typing.Union[ChunkOfText, Emoji, Image]]] = []
        for e in initial_chunks_of_text:
            w: Decimal = e.get_layout_box(
                Rectangle(
                    next_x,
                    available_space.get_y(),
                    available_space.get_width() - line_width,
                    available_space.get_height(),
                )
            ).get_width()
            if (line_width + w > available_space.get_width()) or (
                isinstance(e, LineBreakChunk)
            ):
                # get ready for next line
                lines.append(copy.deepcopy(line))
                next_x = available_space.get_x() + w
                line_width = w
                # fix the one element that does not fit
                assert e._previous_layout_box is not None
                e._previous_layout_box.x = available_space.get_x()
                line = [e]
                continue
            else:
                next_x += w
                line_width += w
                line.append(e)
        if len(line) > 0:
            lines.append(copy.deepcopy(line))

        # update ys
        prev_y: Decimal = available_space.get_y() + available_space.get_height()
        for line in lines:
            line_height: Decimal = max(
                [x.get_previous_layout_box().get_height() for x in line]
            )
            y: Decimal = prev_y - line_height
            for e in line:
                delta_height: Decimal = (
                    line_height - e.get_previous_layout_box().get_height()
                )
                e.get_layout_box(
                    Rectangle(
                        e.get_previous_layout_box().get_x(),
                        y,
                        e.get_previous_layout_box().get_width(),
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
                    line[-1].get_previous_layout_box().get_x()
                    + line[-1].get_previous_layout_box().get_width()
                )
                cbox_max_x = available_space.get_x() + available_space.get_width()
                delta_x = (cbox_max_x - line_max_x) / 2
                for e in line:
                    e._previous_layout_box.x += delta_x

        # update xs (text_alignment == LEFT)
        if self._text_alignment == Alignment.RIGHT:
            for line in lines:
                line_max_x = (
                    line[-1].get_previous_layout_box().get_x()
                    + line[-1].get_previous_layout_box().get_width()
                )
                cbox_max_x = available_space.get_x() + available_space.get_width()
                delta_x = cbox_max_x - line_max_x
                for e in line:
                    e._previous_layout_box.x += delta_x

        # update xs (text_alignment == JUSTIFIED)
        if self._text_alignment == Alignment.JUSTIFIED:
            for line in lines:
                line_max_x = (
                    line[-1].get_previous_layout_box().get_x()
                    + line[-1].get_previous_layout_box().get_width()
                )
                cbox_max_x = available_space.get_x() + available_space.get_width()
                delta_x = (cbox_max_x - line_max_x) / (len(line) - 1)
                for e in line:
                    e._previous_layout_box.x += delta_x

        # return
        return lines

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:

        # lines of text
        lines_of_text: typing.List[
            typing.List[ChunkOfText]
        ] = self._split_to_lines_of_chunks_of_text(available_space)

        # determine height
        h: Decimal = sum(
            [
                max([x.get_previous_layout_box().get_height() for x in line_of_text])
                for line_of_text in lines_of_text
            ]
        )

        # determine width
        w: Decimal = max(
            [
                sum([x.get_previous_layout_box().get_width() for x in line_of_text])
                for line_of_text in lines_of_text
            ]
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
            typing.List[ChunkOfText]
        ] = self._split_to_lines_of_chunks_of_text(available_space)

        for line in lines_of_text:
            for e in line:
                lbox: typing.Optional[Rectangle] = e.get_previous_layout_box()
                assert lbox is not None
                e.paint(page, lbox)
