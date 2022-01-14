#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a generic disjoint shape (specified by a List of lines).
It has convenience methods to calculate width and height, perform scaling, etc
"""

from decimal import Decimal

import typing

from borb.pdf.canvas.color.color import HexColor, Color, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment, LayoutElement
from borb.pdf.page.page import Page


class DisjointShape(LayoutElement):
    """
    This class represents a generic disjoint shape (specified by a List of lines).
    It has convenience methods to calculate width and height, perform scaling, etc
    """

    def __init__(
        self,
        lines: typing.List[
            typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]
        ],
        stroke_color: Color = HexColor("000000"),
        line_width: Decimal = Decimal(0),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        preserve_aspect_ratio: bool = True,
    ):
        super(DisjointShape, self).__init__(
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )
        assert len(lines) > 0
        self._lines = lines
        self._stroke_color = stroke_color
        self._line_width = line_width
        self._preserve_aspect_ratio = preserve_aspect_ratio

    def get_width(self) -> Decimal:
        """
        This function returns the width of this DisjointShape
        """
        min_x = min([min(x[0][0], x[1][0]) for x in self._lines])
        max_x = max([max(x[0][0], x[1][0]) for x in self._lines])
        return max_x - min_x

    def get_height(self) -> Decimal:
        """
        This function returns the height of this DisjointShape
        """
        min_y = min([min(x[0][1], x[1][1]) for x in self._lines])
        max_y = max([max(x[0][1], x[1][1]) for x in self._lines])
        return max_y - min_y

    def scale_to_fit(self, max_width: Decimal, max_height: Decimal) -> "DisjointShape":
        """
        This method scales this DisjointShape to fit a given max. width / height
        """
        w_scale = max_width / self.get_width()
        h_scale = max_height / self.get_height()
        if self._preserve_aspect_ratio:
            w_scale = min(w_scale, h_scale)
            h_scale = w_scale
        if w_scale < 1:
            self._lines = [
                ((x[0][0] * w_scale, x[0][1]), (x[1][0] * w_scale, x[1][1]))
                for x in self._lines
            ]
        if h_scale < 1:
            self._lines = [
                ((x[0][0], x[0][1] * h_scale), (x[1][0], x[1][1] * h_scale))
                for x in self._lines
            ]
        return self

    def translate_to_align(
        self, lower_left_x: Decimal, lower_left_y: Decimal
    ) -> "DisjointShape":
        """
        This method translates this DisjointShape so its lower left corner aligns with the given coordinates
        """
        min_x = min([min(x[0][0], x[1][0]) for x in self._lines])
        min_y = min([min(x[0][1], x[1][1]) for x in self._lines])
        delta_x = lower_left_x - min_x
        delta_y = lower_left_y - min_y
        self._lines = [
            (
                (x[0][0] + delta_x, x[0][1] + delta_y),
                (x[1][0] + delta_x, x[1][1] + delta_y),
            )
            for x in self._lines
        ]
        return self

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # scale to fit
        self.scale_to_fit(bounding_box.width, bounding_box.height)

        # translate points to fit in box
        self.translate_to_align(
            bounding_box.x, bounding_box.y + bounding_box.height - self.get_height()
        )

        # write content
        stroke_rgb = (self._stroke_color or X11Color("Black")).to_rgb()
        content = "q %f %f %f RG %d w " % (
            Decimal(stroke_rgb.red),
            Decimal(stroke_rgb.green),
            Decimal(stroke_rgb.blue),
            self._line_width,
        )
        for l in self._lines:
            content += " %f %f m %f %f l " % (l[0][0], l[0][1], l[1][0], l[1][1])

        # stroke
        content += " S Q"

        # append to page
        self._append_to_content_stream(page, content)

        # calculate bounding box
        layout_rect = Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self.get_height(),
            self.get_width(),
            self.get_height(),
        )

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
