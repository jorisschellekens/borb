#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents a heterogeneous Paragraph.
e.g. a Paragraph where one or more words are in bold (but not all of them)
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page


class LineBreakChunk(ChunkOfText):
    """
    This implementation of ChunkOfText represents a LineBreak
    """

    def __init__(self):
        super(LineBreakChunk, self).__init__("")


class Span(Paragraph):
    """
    This implementation of LayoutElement represents a heterogeneous collection of ChunkOfText elements.
    e.g. a Paragraph where one or more words are in bold (but not all of them)
    """

    def __init__(
        self,
        chunks_of_text: typing.List[ChunkOfText] = [],
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
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
        line_height: Decimal = Decimal(1),
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,  # type: ignore [name-defined]
    ):

        # background color
        self._background_color: typing.Optional[Color] = background_color

        # borders
        self._border_color: Color = border_color
        self._border_width: Decimal = border_width
        self._border_top: bool = border_top
        self._border_right: bool = border_right
        self._border_bottom: bool = border_bottom
        self._border_left: bool = border_left

        # alignment
        self._horizontal_alignment = horizontal_alignment
        self._vertical_alignment = vertical_alignment

        # padding
        self._padding_top: Decimal = padding_top
        self._padding_right: Decimal = padding_right
        self._padding_bottom: Decimal = padding_bottom
        self._padding_left: Decimal = padding_left

        # margin
        self._margin_top: typing.Optional[Decimal] = margin_top
        self._margin_right: typing.Optional[Decimal] = margin_right
        self._margin_bottom: typing.Optional[Decimal] = margin_bottom
        self._margin_left: typing.Optional[Decimal] = margin_left

        # leading
        self._font_size: typing.Optional[Decimal] = None
        assert line_height >= Decimal(1)
        self._line_height: Decimal = line_height

        # store chunks
        self._chunks_of_text: typing.List[ChunkOfText] = []
        for c in chunks_of_text:
            self.add(c)

    def add(self, chunk_of_text: typing.Union[ChunkOfText, "Span"]) -> "Span":
        """
        This function adds a ChunkOfText to this heterogeneous Paragraph.
        This function returns self.
        """
        if isinstance(chunk_of_text, Span):
            for c in chunk_of_text._chunks_of_text:
                self.add(c)
            return self
        self._chunks_of_text.append(chunk_of_text)
        if self._font_size is None:
            self._font_size = self._chunks_of_text[0].get_font_size()
        return self

    def add_line_break(self) -> "Span":
        """
        This function adds a LineBreakChunk to this heterogeneous Paragraph.
        This function returns self.
        """
        return self.add(LineBreakChunk())

    def _split_chunks_to_lines(
        self, page: Page, bounding_box: Rectangle
    ) -> typing.List[typing.Tuple[typing.List[ChunkOfText], Decimal]]:
        lines: typing.List[typing.Tuple[typing.List[ChunkOfText], Decimal]] = []
        previous_line: typing.List[ChunkOfText] = []
        previous_line_width: Decimal = Decimal(0)
        for i in range(0, len(self._chunks_of_text)):
            c: ChunkOfText = self._chunks_of_text[i]
            # process LineBreakChunk
            if isinstance(c, LineBreakChunk):
                if len(previous_line) > 0:
                    lines.append(([x for x in previous_line], previous_line_width))
                previous_line.clear()
                previous_line_width = Decimal(0)
                continue
            # process ChunkOfText
            w: Decimal = c._calculate_layout_box_without_padding(
                page, bounding_box
            ).get_width()
            if round(previous_line_width + w, 2) > round(bounding_box.get_width(), 2):
                lines.append(([x for x in previous_line], previous_line_width))
                previous_line.clear()
                previous_line.append(c)
                previous_line_width = w
            else:
                previous_line.append(c)
                previous_line_width += w
        if len(previous_line) > 0:
            lines.append(([x for x in previous_line], previous_line_width))
        return lines

    def _do_layout_without_padding(self, page: Page, bounding_box: Rectangle):

        # split text to lines
        lines: typing.List[
            typing.Tuple[typing.List[ChunkOfText], Decimal]
        ] = self._split_chunks_to_lines(page, bounding_box)

        assert self._horizontal_alignment in [
            Alignment.LEFT,
            Alignment.RIGHT,
            Alignment.CENTERED,
        ]

        #
        min_x: Decimal = Decimal(2048)
        min_y: Decimal = Decimal(2048)
        max_x: Decimal = Decimal(0)
        max_y: Decimal = Decimal(0)

        # determine y-coordinate for line
        line_y: Decimal = (
            bounding_box.get_y()
            + bounding_box.get_height()
            - max([x.get_bounding_box().get_height() for x in lines[0][0]])  # type: ignore [union-attr]
        )

        for line_of_chunks, line_width in lines:

            # determine x-coordinate to start line
            prev_x: Decimal = bounding_box.get_x()
            if self._horizontal_alignment == Alignment.LEFT:
                prev_x = bounding_box.get_x()
            elif self._horizontal_alignment == Alignment.RIGHT:
                # fmt: off
                prev_x = bounding_box.get_x() + bounding_box.get_width() - line_width
                # fmt: on
            elif self._horizontal_alignment == Alignment.CENTERED:
                # fmt: off
                prev_x = bounding_box.get_x() + (bounding_box.get_width() - line_width) / Decimal(2)
                # fmt: on

            # layout line
            for chunk_of_text in line_of_chunks:
                r: Rectangle = chunk_of_text.layout(
                    page,
                    Rectangle(
                        prev_x,
                        line_y,
                        bounding_box.get_width(),
                        chunk_of_text.get_font_size(),
                    ),
                )

                # update prev_x
                assert r is not None
                prev_x += r.get_width()

                # keep track of layout coordinates
                # to determine the final layout rectangle of this pseudo-paragraph
                min_x = min(r.x, min_x)
                min_y = min(r.y, min_y)
                max_x = max(r.x + r.width, max_x)
                max_y = max(r.y + r.height, max_y)

            # update line_y
            line_y -= (
                max([x.get_bounding_box().get_height() for x in line_of_chunks])  # type: ignore [union-attr]
                * self._line_height
            )

        layout_rect = Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect


class HeterogeneousParagraph(Span):
    """
    This implementation of LayoutElement represents a heterogeneous collection of ChunkOfText elements.
    Furthermore (like Paragraph, and unlike Span), this element has a default top- and bottom margin.
    e.g. a Paragraph where one or more words are in bold (but not all of them)
    """

    def __init__(
        self,
        chunks_of_text: typing.List[ChunkOfText] = [],
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
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
        line_height: Decimal = Decimal(1),
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,  # type: ignore [name-defined]
    ):
        super(HeterogeneousParagraph, self).__init__(
            chunks_of_text=chunks_of_text,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
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
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            line_height=line_height,
            background_color=background_color,
            parent=parent,
        )

    def add(
        self, chunk_of_text: typing.Union[ChunkOfText, "HeterogeneousParagraph"]
    ) -> "HeterogeneousParagraph":
        """
        This function adds a ChunkOfText to this heterogeneous Paragraph.
        This function returns self.
        """
        if isinstance(chunk_of_text, HeterogeneousParagraph):
            for c in chunk_of_text._chunks_of_text:
                self.add(c)
            return self
        self._chunks_of_text.append(chunk_of_text)
        if self._font_size is None:
            self._font_size = self._chunks_of_text[0].get_font_size()
        if self._margin_top is None:
            self._margin_top = self._font_size
        if self._margin_bottom is None:
            self._margin_bottom = self._font_size
        return self
