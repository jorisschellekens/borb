#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a generic shape (specified by a List of points).
It has convenience methods to calculate width and height, perform scaling, etc
"""
import math
import typing
from decimal import Decimal
from math import sqrt
from typing import Tuple

from borb.pdf.canvas.color.color import Color, HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment, LayoutElement
from borb.pdf.page.page import Page


class Shape(LayoutElement):
    """
    This class represents a generic shape (specified by a List of points).
    It has convenience methods to calculate width and height, perform scaling, etc
    """

    def __init__(
        self,
        points: typing.List[Tuple[Decimal, Decimal]],
        fill_color: typing.Optional[Color],
        stroke_color: typing.Optional[Color],
        auto_close_shape: bool = False,
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
        horizontal_alignment: Alignment = Alignment.LEFT,
        line_width: Decimal = Decimal(1),
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(Shape, self).__init__(
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
            font_size=Decimal(12),
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        assert len(points) >= 3
        self._points = points
        self._stroke_color = stroke_color
        self._fill_color = fill_color
        assert line_width >= Decimal(0)
        self._line_width = line_width

        # close shape if desired (and needed)
        if (
            auto_close_shape
            and sqrt(
                (points[0][0] - points[-1][0]) ** 2
                + (points[0][1] - points[-1][1]) ** 2
            )
            > 0.00000001
        ):
            points.append(points[0])

    def get_width(self) -> Decimal:
        """
        This function returns the width of this Shape
        """
        min_x = min([x[0] for x in self._points])
        max_x = max([x[0] for x in self._points])
        return max_x - min_x

    def get_height(self) -> Decimal:
        """
        This function returns the height of this Shape
        """
        min_y = min([x[1] for x in self._points])
        max_y = max([x[1] for x in self._points])
        return max_y - min_y

    def scale_down(
        self,
        max_width: Decimal,
        max_height: Decimal,
        preserve_aspect_ratio: bool = True,
    ) -> "Shape":
        """
        This method scales this Shape down to fit a given max. width / height
        """
        w_scale = max_width / self.get_width()
        h_scale = max_height / self.get_height()
        if preserve_aspect_ratio:
            w_scale = min(w_scale, h_scale)
            h_scale = w_scale
        if w_scale < 1:
            self._points = [(x[0] * w_scale, x[1]) for x in self._points]
        if h_scale < 1:
            self._points = [(x[0], x[1] * h_scale) for x in self._points]
        return self

    def scale_up(
        self,
        max_width: Decimal,
        max_height: Decimal,
        preserve_aspect_ratio: bool = True,
    ) -> "Shape":
        """
        This method scales this Shape up to fit a given max. width / height
        """
        w_scale = max_width / self.get_width()
        h_scale = max_height / self.get_height()
        if preserve_aspect_ratio:
            w_scale = min(w_scale, h_scale)
            h_scale = w_scale
        if w_scale > 1:
            self._points = [(x[0] * w_scale, x[1]) for x in self._points]
        if h_scale > 1:
            self._points = [(x[0], x[1] * h_scale) for x in self._points]
        return self

    def rotate(self, angle_in_radians: float) -> "Shape":
        """
        This function rotates the Shape for a given angle
        :param angle_in_radians:    the angle
        :return:                    this Shape
        """
        a: Decimal = Decimal(math.cos(angle_in_radians))
        b: Decimal = Decimal(-math.sin(angle_in_radians))
        c: Decimal = Decimal(math.sin(angle_in_radians))
        d: Decimal = Decimal(math.cos(angle_in_radians))
        self._points = [(a * x + c * y, b * x + d * y) for x, y in self._points]
        return self

    def move_to(self, lower_left_x: Decimal, lower_left_y: Decimal) -> "Shape":
        """
        This method translates this Shape so its lower left corner aligns with the given coordinates
        """
        min_x = min([x[0] for x in self._points])
        min_y = min([x[1] for x in self._points])
        delta_x = lower_left_x - min_x
        delta_y = lower_left_y - min_y
        self._points = [(x[0] + delta_x, x[1] + delta_y) for x in self._points]
        return self

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # translate points to fit in box
        self.move_to(
            bounding_box.x, bounding_box.y + bounding_box.height - self.get_height()
        )

        # write content
        stroke_rgb = (self._stroke_color or HexColor("000000")).to_rgb()
        fill_rgb = (self._fill_color or HexColor("ffffff")).to_rgb()
        content = "q %f %f %f RG  %f %f %f rg %f w " % (
            Decimal(stroke_rgb.red),
            Decimal(stroke_rgb.green),
            Decimal(stroke_rgb.blue),
            Decimal(fill_rgb.red),
            Decimal(fill_rgb.green),
            Decimal(fill_rgb.blue),
            self._line_width,
        )
        content += "%f %f m " % (self._points[0][0], self._points[0][1])
        for p in self._points[1:]:
            content += " %f %f l " % (p[0], p[1])

        operator: str = "B"
        if self._stroke_color is None:
            operator = "F"
        if self._fill_color is None:
            operator = "S"
        content += " %s " % operator
        content += " Q"

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
