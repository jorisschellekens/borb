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

from ptext.io.read.types import Decimal as pDecimal
from ptext.io.read.types import Stream, Name
from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import Page


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
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,
    ):
        # borders
        self.border_top = border_top
        self.border_right = border_right
        self.border_bottom = border_bottom
        self.border_left = border_left
        assert border_width >= 0
        self.border_width = border_width
        self.border_color = border_color

        # padding
        assert padding_top >= 0
        assert padding_right >= 0
        assert padding_bottom >= 0
        assert padding_left >= 0
        self.padding_top = padding_top
        self.padding_right = padding_right
        self.padding_bottom = padding_bottom
        self.padding_left = padding_left

        # alignment
        assert horizontal_alignment in [
            Alignment.LEFT,
            Alignment.CENTERED,
            Alignment.RIGHT,
            Alignment.JUSTIFIED,
        ]
        assert vertical_alignment in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment

        # background color
        self.background_color = background_color

        # linkage (for lists, tables, etc)
        self.parent = parent

        # layout
        self.bounding_box: typing.Optional[Rectangle] = None

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

    def _initialize_page_content_stream(self, page: Page):
        if "Contents" in page:
            return

        # build content stream object
        content_stream = Stream()
        content_stream[Name("DecodedBytes")] = b""
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Filter")] = Name("FlateDecode")
        content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

        # set content of page
        page[Name("Contents")] = content_stream

    def _append_to_content_stream(self, page: Page, instructions: str):
        self._initialize_page_content_stream(page)
        content_stream = page["Contents"]
        content_stream[Name("DecodedBytes")] += instructions.encode("latin1")
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

    def _calculate_layout_box(self, page: Page, bounding_box: Rectangle) -> Rectangle:

        # modify bounding box (to take into account padding)
        modified_bounding_box = Rectangle(
            bounding_box.x + self.padding_left,
            bounding_box.y + self.padding_bottom,
            max(
                bounding_box.width - self.padding_right - self.padding_left, Decimal(0)
            ),
            max(
                bounding_box.height - self.padding_top - self.padding_bottom, Decimal(0)
            ),
        )

        # delegate
        layout_rect = self._calculate_layout_box_without_padding(
            page, modified_bounding_box
        )

        # modify rectangle (to take into account padding)
        modified_layout_rect = Rectangle(
            layout_rect.x - self.padding_left,
            layout_rect.y - self.padding_bottom,
            layout_rect.width + self.padding_left + self.padding_right,
            layout_rect.height + self.padding_top + self.padding_bottom,
        )

        # return
        return modified_layout_rect

    def _calculate_layout_box_without_padding(
        self, page: Page, bounding_box: Rectangle
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

    def _do_layout(self, page: Page, layout_box: Rectangle) -> Rectangle:

        # modify bounding box (to take into account padding)
        modified_bounding_box = Rectangle(
            layout_box.x + self.padding_left,
            layout_box.y + self.padding_bottom,
            max(layout_box.width - self.padding_right - self.padding_left, Decimal(0)),
            max(layout_box.height - self.padding_top - self.padding_bottom, Decimal(0)),
        )

        # delegate
        output_box = self._do_layout_without_padding(page, modified_bounding_box)

        # modify rectangle (to take into account padding)
        modified_layout_rect = Rectangle(
            output_box.x - self.padding_left,
            output_box.y - self.padding_bottom,
            output_box.width + self.padding_left + self.padding_right,
            output_box.height + self.padding_top + self.padding_bottom,
        )

        # draw border
        self._draw_border(page, modified_layout_rect)

        # return
        return modified_layout_rect

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:
        """
        This function calculates the layout box and performs layout for this LayoutElement.
        e.g. for a Paragraph this might involve taking into account the word hyphenation,
        and enforcing vertical and horizontal alignment.
        """
        return self.calculate_layout_box_and_do_layout(page, bounding_box)

    def calculate_layout_box_and_do_layout(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        """
        This function calculates the layout box and performs layout for this LayoutElement.
        e.g. for a Paragraph this might involve taking into account the word hyphenation,
        and enforcing vertical and horizontal alignment.
        """

        # calculate initial layout box
        layout_box = self._calculate_layout_box(page, bounding_box)

        content_stream = page["Contents"]
        len_decoded_bytes_before = len(content_stream[Name("DecodedBytes")])

        # set the vertical alignment
        if self.vertical_alignment == Alignment.MIDDLE:
            bounding_box = Rectangle(
                bounding_box.x,
                bounding_box.y,
                bounding_box.width,
                bounding_box.height
                - bounding_box.height / Decimal(2)
                + layout_box.height / Decimal(2),
            )
        if self.vertical_alignment == Alignment.BOTTOM:
            bounding_box = Rectangle(
                bounding_box.x,
                bounding_box.y,
                bounding_box.width,
                layout_box.height,
            )

        # set the horizontal alignment
        if self.horizontal_alignment == Alignment.CENTERED:
            bounding_box = Rectangle(
                bounding_box.x + (bounding_box.width - layout_box.width) / Decimal(2),
                bounding_box.y,
                layout_box.width,
                bounding_box.height,
            )
        if self.horizontal_alignment == Alignment.RIGHT:
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
        if self.background_color is not None:

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
        self, page: Page, layout_box: Rectangle
    ) -> Rectangle:
        return Rectangle(layout_box.x, layout_box.y, Decimal(0), Decimal(0))

    def _draw_background(self, page: Page, border_box: Rectangle):
        if not self.background_color:
            return
        assert self.background_color
        rgb_color = self.background_color.to_rgb()
        COLOR_MAX = Decimal(255.0)
        content = """
            q %f %f %f rg %f %f m %f %f l %f %f l %f %f l f Q
            """ % (
            Decimal(rgb_color.red / COLOR_MAX),
            Decimal(rgb_color.green / COLOR_MAX),
            Decimal(rgb_color.blue / COLOR_MAX),
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

    def _draw_border(self, page: Page, border_box: Rectangle):
        # border is not wanted on any side
        if (
            self.border_top
            == self.border_right
            == self.border_bottom
            == self.border_right
            == False
        ):
            return

        # border width is set to zero
        if self.border_width == 0:
            return

        # print("R %f %f %f %f " % (border_box.x, border_box.y, border_box.width, border_box.height))

        # draw border(s)
        rgb_color = self.border_color.to_rgb()
        COLOR_MAX = Decimal(255.0)
        content = "q %f %f %f RG %f w" % (
            Decimal(rgb_color.red / COLOR_MAX),
            Decimal(rgb_color.green / COLOR_MAX),
            Decimal(rgb_color.blue / COLOR_MAX),
            self.border_width,
        )
        if self.border_top:
            content += " %f %f m %f %f l s" % (
                border_box.x,
                border_box.y + border_box.height,
                border_box.x + border_box.width,
                border_box.y + border_box.height,
            )
        if self.border_right:
            content += " %d %d m %d %d l s" % (
                border_box.x + border_box.width,
                border_box.y + border_box.height,
                border_box.x + border_box.width,
                border_box.y,
            )
        if self.border_bottom:
            content += " %d %d m %d %d l s" % (
                border_box.x + border_box.width,
                border_box.y,
                border_box.x,
                border_box.y,
            )
        if self.border_left:
            content += " %d %d m %d %d l s" % (
                border_box.x,
                border_box.y,
                border_box.x,
                border_box.y + border_box.height,
            )
        content += " Q "
        self._append_to_content_stream(page, content)
