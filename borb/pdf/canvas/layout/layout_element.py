#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains all the classes needed to perform layout.
This includes an Alignment Enum type, and the base implementation of LayoutElement
"""
import typing
import zlib
from decimal import Decimal
from enum import Enum

from borb.io.read.types import Decimal as pDecimal
from borb.io.read.types import Dictionary, Name, Stream
from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle


class Alignment(Enum):
    """
    In typesetting and page layout, alignment or range is the setting of text flow or image placement relative to a page,
    column (measure), table cell, or tab.
    The type alignment setting is sometimes referred to as text alignment,
    text justification, or type justification.
    The edge of a page or column is known as a margin, and a gap between columns is known as a gutter.
    """

    LEFT = 2
    CENTERED = 3
    RIGHT = 5
    JUSTIFIED = 7

    TOP = 11
    MIDDLE = 13
    BOTTOM = 17


class LayoutElement:
    """
    This class contains the common base methods for any object that can be laid out on a Page.
    e.g. the placement of borders, margins, padding, background color, etc
    """

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        font_size: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        parent: typing.Optional["LayoutElement"] = None,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        # background color
        self._background_color = background_color

        # borders
        self._border_top = border_top
        self._border_right = border_right
        self._border_bottom = border_bottom
        self._border_left = border_left
        assert border_width >= 0
        self._border_width = border_width
        self._border_color = border_color

        # font_size
        self._font_size = font_size

        # margin
        assert margin_top is None or margin_top >= 0
        assert margin_right is None or margin_right >= 0
        assert margin_bottom is None or margin_bottom >= 0
        assert margin_left is None or margin_left >= 0
        self._margin_top = margin_top
        self._margin_right = margin_right
        self._margin_bottom = margin_bottom
        self._margin_left = margin_left

        # padding
        assert padding_top >= 0
        assert padding_right >= 0
        assert padding_bottom >= 0
        assert padding_left >= 0
        self._padding_top = padding_top
        self._padding_right = padding_right
        self._padding_bottom = padding_bottom
        self._padding_left = padding_left

        # alignment
        assert horizontal_alignment in [
            Alignment.LEFT,
            Alignment.CENTERED,
            Alignment.RIGHT,
            Alignment.JUSTIFIED,
        ]
        assert vertical_alignment in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]
        self._horizontal_alignment = horizontal_alignment
        self._vertical_alignment = vertical_alignment

        # linkage (for lists, tables, etc)
        self._parent = parent

        # layout
        self.bounding_box: typing.Optional[Rectangle] = None

    def get_font_size(self) -> Decimal:
        """
        This function returns the font size of this LayoutElement
        """
        return self._font_size or Decimal(0)

    def get_margin_top(self) -> Decimal:
        """
        This function returns the top margin of this LayoutElement
        """
        return self._margin_top or Decimal(0)

    def get_margin_right(self) -> Decimal:
        """
        This function returns the right margin of this LayoutElement
        """
        return self._margin_right or Decimal(0)

    def get_margin_bottom(self) -> Decimal:
        """
        This function returns the bottom margin of this LayoutElement
        """
        return self._margin_bottom or Decimal(0)

    def get_margin_left(self) -> Decimal:
        """
        This function returns the left margin of this LayoutElement
        """
        return self._margin_left or Decimal(0)

    def set_bounding_box(self, bounding_box: Rectangle) -> "LayoutElement":
        """
        This method sets the bounding box of this LayoutElement
        """
        self.bounding_box = bounding_box
        return self

    def get_bounding_box(self) -> typing.Optional[Rectangle]:
        """
        This function returns the bounding box of this LayoutElement
        """
        return self.bounding_box

    def _initialize_page_content_stream(self, page: "Page"):  # type: ignore[name-defined]

        # build content stream object
        if "Contents" not in page:
            content_stream = Stream()
            content_stream[Name("DecodedBytes")] = b""
            content_stream[Name("Bytes")] = zlib.compress(
                content_stream["DecodedBytes"], 9
            )
            content_stream[Name("Filter")] = Name("FlateDecode")
            content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

            # set content of page
            page[Name("Contents")] = content_stream

        # set Resources
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary()

    def _append_to_content_stream(self, page: "Page", instructions: str):  # type: ignore[name-defined]
        self._initialize_page_content_stream(page)
        content_stream = page["Contents"]

        # prepend whitespace if needed
        if len(content_stream[Name("DecodedBytes")]) != 0:
            # fmt: off
            decoded_bytes_last_char: str = str(content_stream["DecodedBytes"][-1:], encoding="latin1")
            if decoded_bytes_last_char not in [" ", "\t", "\n"] and instructions[0] not in [" ", "\t", "\n"]:
                instructions = " " + instructions
            # fmt: on

        content_stream[Name("DecodedBytes")] += instructions.encode("latin1")
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

    def _calculate_layout_box(self, page: "Page", bounding_box: Rectangle) -> Rectangle:  # type: ignore[name-defined]

        # modify bounding box (to take into account padding)
        modified_layout_box = Rectangle(
            bounding_box.x + self._padding_left,
            bounding_box.y + self._padding_bottom,
            max(
                bounding_box.width - self._padding_right - self._padding_left,
                Decimal(0),
            ),
            max(
                bounding_box.height - self._padding_top - self._padding_bottom,
                Decimal(0),
            ),
        )

        # delegate
        returned_layout_box = self._calculate_layout_box_without_padding(
            page, modified_layout_box
        )

        # modify rectangle (to take into account padding)
        modified_returned_layout_box = Rectangle(
            returned_layout_box.x - self._padding_left,
            returned_layout_box.y - self._padding_bottom,
            returned_layout_box.width + self._padding_left + self._padding_right,
            returned_layout_box.height + self._padding_top + self._padding_bottom,
        )

        # set
        self.set_bounding_box(modified_returned_layout_box)

        # return
        return modified_returned_layout_box

    def _calculate_layout_box_without_padding(
        self, page: "Page", bounding_box: Rectangle  # type: ignore[name-defined]
    ) -> Rectangle:

        # store previous contents
        if "Contents" not in page:
            self._initialize_page_content_stream(page)
        previous_decoded_bytes = page["Contents"]["DecodedBytes"]

        # layout without padding
        layout_rect = self._do_layout_without_padding(page, bounding_box)
        assert layout_rect is not None

        # restore
        content_stream = page["Contents"]
        content_stream[Name("DecodedBytes")] = previous_decoded_bytes
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

        # return
        return layout_rect

    def _do_layout(self, page: "Page", layout_box: Rectangle) -> Rectangle:  # type: ignore[name-defined]

        # modify bounding box (to take into account padding)
        modified_bounding_box = Rectangle(
            layout_box.x + self._padding_left,
            layout_box.y + self._padding_bottom,
            max(
                layout_box.width - self._padding_right - self._padding_left, Decimal(0)
            ),
            max(
                layout_box.height - self._padding_top - self._padding_bottom, Decimal(0)
            ),
        )

        # delegate
        output_box = self._do_layout_without_padding(page, modified_bounding_box)

        # modify rectangle (to take into account padding)
        modified_layout_rect = Rectangle(
            output_box.x - self._padding_left,
            output_box.y - self._padding_bottom,
            output_box.width + self._padding_left + self._padding_right,
            output_box.height + self._padding_top + self._padding_bottom,
        )

        # draw border
        self._draw_border(page, modified_layout_rect)

        # return
        return modified_layout_rect

    def layout(self, page: "Page", bounding_box: Rectangle) -> Rectangle:  # type: ignore[name-defined]
        """
        This function calculates the layout box and performs layout for this LayoutElement.
        e.g. for a Paragraph this might involve taking into account the word hyphenation,
        and enforcing vertical and horizontal alignment.
        """
        return self.calculate_layout_box_and_do_layout(page, bounding_box)

    def calculate_layout_box_and_do_layout(
        self, page: "Page", bounding_box: Rectangle  # type: ignore[name-defined]
    ) -> Rectangle:
        """
        This function calculates the layout box and performs layout for this LayoutElement.
        e.g. for a Paragraph this might involve taking into account the word hyphenation,
        and enforcing vertical and horizontal alignment.
        """

        # calculate initial layout box
        self._initialize_page_content_stream(page)
        layout_box = self._calculate_layout_box(page, bounding_box)

        content_stream = page["Contents"]
        len_decoded_bytes_before = len(content_stream[Name("DecodedBytes")])

        # set the vertical alignment
        if self._vertical_alignment == Alignment.MIDDLE:
            bounding_box = Rectangle(
                bounding_box.x,
                bounding_box.y,
                bounding_box.width,
                bounding_box.height
                - bounding_box.height / Decimal(2)
                + layout_box.height / Decimal(2),
            )
        if self._vertical_alignment == Alignment.BOTTOM:
            bounding_box = Rectangle(
                bounding_box.x,
                bounding_box.y,
                bounding_box.width,
                layout_box.height,
            )

        # set the horizontal alignment
        if self._horizontal_alignment == Alignment.CENTERED:
            bounding_box = Rectangle(
                bounding_box.x + (bounding_box.width - layout_box.width) / Decimal(2),
                bounding_box.y,
                layout_box.width,
                bounding_box.height,
            )
        if self._horizontal_alignment == Alignment.RIGHT:
            bounding_box = Rectangle(
                bounding_box.x + (bounding_box.width - layout_box.width),
                bounding_box.y,
                layout_box.width,
                bounding_box.height,
            )

        # perform layout
        final_layout_box = self._do_layout(page, bounding_box)
        self.set_bounding_box(final_layout_box)

        # add background
        if self._background_color is not None:

            # change content stream to put background before rendering of the content
            added_content = content_stream[Name("DecodedBytes")][
                len_decoded_bytes_before:
            ]
            content_stream[Name("DecodedBytes")] = content_stream[Name("DecodedBytes")][
                0:len_decoded_bytes_before
            ]

            # add background
            self._draw_background(page, final_layout_box)

            # re-add content
            content_stream[Name("DecodedBytes")] += added_content
            content_stream[Name("Bytes")] = zlib.compress(
                content_stream[Name("DecodedBytes")], 9
            )
            content_stream[Name("Length")] = len(content_stream[Name("Bytes")])

        return final_layout_box

    def _do_layout_without_padding(
        self, page: "Page", layout_box: Rectangle  # type: ignore[name-defined]
    ) -> Rectangle:
        return Rectangle(layout_box.x, layout_box.y, Decimal(0), Decimal(0))

    def _draw_background(self, page: "Page", border_box: Rectangle):  # type: ignore[name-defined]
        if not self._background_color:
            return
        assert self._background_color
        rgb_color = self._background_color.to_rgb()
        content = """
            q %f %f %f rg %f %f m %f %f l %f %f l %f %f l f Q
            """ % (
            Decimal(rgb_color.red),
            Decimal(rgb_color.green),
            Decimal(rgb_color.blue),
            border_box.x,  # lower left corner
            border_box.y,  # lower left corner
            border_box.x + border_box.width,  # lower right corner
            border_box.y,  # lower right corner
            border_box.x + border_box.width,  # upper right corner
            border_box.y + border_box.height,  # upper right corner
            border_box.x,  # upper left corner
            border_box.y + border_box.height,  # upper left corner
        )
        self._append_to_content_stream(page, content)

    def _draw_border(self, page: "Page", border_box: Rectangle):  # type: ignore[name-defined]
        # border is not wanted on any side
        if (
            self._border_top
            == self._border_right
            == self._border_bottom
            == self._border_left
            == False
        ):
            return

        # border width is set to zero
        if self._border_width == 0:
            return

        # print("R %f %f %f %f " % (border_box.x, border_box.y, border_box.width, border_box.height))

        # draw border(s)
        rgb_color = self._border_color.to_rgb()
        content = "q %f %f %f RG %f w" % (
            Decimal(rgb_color.red),
            Decimal(rgb_color.green),
            Decimal(rgb_color.blue),
            self._border_width,
        )
        if self._border_top:
            content += " %f %f m %f %f l s" % (
                border_box.x,
                border_box.y + border_box.height,
                border_box.x + border_box.width,
                border_box.y + border_box.height,
            )
        if self._border_right:
            content += " %d %d m %d %d l s" % (
                border_box.x + border_box.width,
                border_box.y + border_box.height,
                border_box.x + border_box.width,
                border_box.y,
            )
        if self._border_bottom:
            content += " %d %d m %d %d l s" % (
                border_box.x + border_box.width,
                border_box.y,
                border_box.x,
                border_box.y,
            )
        if self._border_left:
            content += " %d %d m %d %d l s" % (
                border_box.x,
                border_box.y,
                border_box.x,
                border_box.y + border_box.height,
            )
        content += " Q "
        self._append_to_content_stream(page, content)
