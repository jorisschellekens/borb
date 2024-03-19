#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a generic disjoint shape (specified by a List of lines).
It has convenience methods to calculate width and height, perform scaling, etc
"""
import math
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class DisconnectedShape(LayoutElement):
    """
    This class represents a generic disjoint shape (specified by a List of lines).
    It has convenience methods to calculate width and height, perform scaling, etc
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        lines: typing.List[
            typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]
        ],
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
        stroke_color: Color = HexColor("000000"),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(DisconnectedShape, self).__init__(
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
            font="Helvetica",
            font_color=HexColor("#000000"),
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
        assert len(lines) > 0
        self._lines = lines
        self._stroke_color = stroke_color
        self._line_width = line_width

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - self.get_height(),
            self.get_width(),
            self.get_height(),
        )

    def _paint_content_box(self, page: Page, available_space: Rectangle) -> None:
        # translate points to fit in box
        self.move_to(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - self.get_height(),
        )

        # write content
        stroke_rgb = (self._stroke_color or HexColor("000000")).to_rgb()
        content = "q %f %f %f RG %d w " % (
            float(stroke_rgb.red),
            float(stroke_rgb.green),
            float(stroke_rgb.blue),
            float(self._line_width),
        )
        for l in self._lines:
            content += " %f %f m %f %f l " % (
                float(l[0][0]),
                float(l[0][1]),
                float(l[1][0]),
                float(l[1][1]),
            )

        # stroke
        content += " S Q"

        # append to page
        page.append_to_content_stream(content)

    #
    # PUBLIC
    #

    def get_height(self) -> Decimal:
        """
        This function returns the height of this DisjointShape
        :return:    the height
        """
        min_y = min([min(x[0][1], x[1][1]) for x in self._lines])
        max_y = max([max(x[0][1], x[1][1]) for x in self._lines])
        return max_y - min_y

    def get_width(self) -> Decimal:
        """
        This function returns the width of this DisjointShape
        :return:    the width
        """
        min_x = min([min(x[0][0], x[1][0]) for x in self._lines])
        max_x = max([max(x[0][0], x[1][0]) for x in self._lines])
        return max_x - min_x

    def move_to(
        self, lower_left_x: Decimal, lower_left_y: Decimal
    ) -> "DisconnectedShape":
        """
        This method translates this Shape so its lower left corner aligns with the given coordinates
        :param lower_left_x:    the desired lower left x-coordinate
        :param lower_left_y:    the desired lower left y-coordinate
        :return:    self
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

    def rotate(self, angle_in_radians: float) -> "Shape":  # type: ignore[name-defined]
        """
        This function rotates the DisjointShape for a given angle
        :param angle_in_radians:    the angle
        :return:                    self
        """
        a: Decimal = Decimal(math.cos(angle_in_radians))
        b: Decimal = Decimal(-math.sin(angle_in_radians))
        c: Decimal = Decimal(math.sin(angle_in_radians))
        d: Decimal = Decimal(math.cos(angle_in_radians))
        self._lines = [
            (
                (a * l[0][0] + c * l[0][1], b * l[0][0] + d * l[0][1]),
                (a * l[1][0] + c * l[1][1], b * l[1][0] + d * l[1][1]),
            )
            for l in self._lines
        ]
        return self

    def scale_down(
        self,
        max_width: Decimal,
        max_height: Decimal,
        preserve_aspect_ratio: bool = True,
    ) -> "DisconnectedShape":
        """
        This method scales this Shape down to fit a given max. width / height
        :param max_width:               the maximum width
        :param max_height:              the maximum height
        :param preserve_aspect_ratio:   True if the aspect ratio should be preserved, False otherwise
        :return:                        self
        """
        w_scale = max_width / self.get_width()
        h_scale = max_height / self.get_height()
        if preserve_aspect_ratio:
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

    def scale_up(
        self,
        max_width: Decimal,
        max_height: Decimal,
        preserve_aspect_ratio: bool = True,
    ) -> "DisconnectedShape":
        """
        This method scales this Shape up to fit a given max. width / height
        :param max_width:               the maximum width
        :param max_height:              the maximum height
        :param preserve_aspect_ratio:   True if the aspect ratio should be preserved, False otherwise
        :return:                        self
        """
        w_scale = max_width / self.get_width()
        h_scale = max_height / self.get_height()
        if preserve_aspect_ratio:
            w_scale = min(w_scale, h_scale)
            h_scale = w_scale
        if w_scale > 1:
            self._lines = [
                ((x[0][0] * w_scale, x[0][1]), (x[1][0] * w_scale, x[1][1]))
                for x in self._lines
            ]
        if h_scale > 1:
            self._lines = [
                ((x[0][0], x[0][1] * h_scale), (x[1][0], x[1][1] * h_scale))
                for x in self._lines
            ]
        return self
