#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class represents a collection of shqpes (objects of type ConnectedShape or DisconnectedShape).
It has convenience methods to calculate width and height, perform scaling, etc
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape


class Shapes(LayoutElement):
    """
    This class represents a collection of shapes (objects of type ConnectedShape or DisconnectedShape).
    It has convenience methods to calculate width and height, perform scaling, etc
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        shapes: typing.List[typing.Union[ConnectedShape, DisconnectedShape]],
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
        fill_color: typing.Optional[Color] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        line_width: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        stroke_color: typing.Optional[Color] = None,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(Shapes, self).__init__(
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
        self._shapes: typing.List[
            typing.Union[ConnectedShape, DisconnectedShape]
        ] = shapes
        for s in self._shapes:
            if line_width is not None:
                s._line_width = line_width
            if isinstance(s, ConnectedShape):
                if fill_color is not None:
                    s._fill_color = fill_color
                if stroke_color is not None:
                    s._stroke_color = stroke_color
            if isinstance(s, DisconnectedShape):
                if stroke_color is not None:
                    s._stroke_color = stroke_color

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

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:  # type: ignore[name-defined]

        # translate points to fit in box
        self.move_to(
            content_box.get_x(),
            content_box.get_y() + content_box.get_height() - self.get_height(),
        )

        # set up content instruction(s)
        content: str = ""
        for cs in self._shapes:
            if isinstance(cs, ConnectedShape):
                stroke_rgb = (cs._stroke_color or HexColor("000000")).to_rgb()
                fill_rgb = (cs._fill_color or HexColor("ffffff")).to_rgb()
                content += " q %f %f %f RG  %f %f %f rg %f w " % (
                    float(stroke_rgb.red),
                    float(stroke_rgb.green),
                    float(stroke_rgb.blue),
                    float(fill_rgb.red),
                    float(fill_rgb.green),
                    float(fill_rgb.blue),
                    float(cs._line_width),
                )
                content += "%f %f m " % (
                    float(cs._points[0][0]),
                    float(cs._points[0][1]),
                )
                for p in cs._points[1:]:
                    content += " %f %f l " % (float(p[0]), float(p[1]))
                operator: str = "B"
                if cs._stroke_color is None:
                    operator = "F"
                if cs._fill_color is None:
                    operator = "S"
                content += " %s " % operator
                content += " Q "
            if isinstance(cs, DisconnectedShape):
                stroke_rgb = (cs._stroke_color or HexColor("000000")).to_rgb()
                content += " q %f %f %f RG %d w " % (
                    float(stroke_rgb.red),
                    float(stroke_rgb.green),
                    float(stroke_rgb.blue),
                    float(cs._line_width),
                )
                for l in cs._lines:
                    content += " %f %f m %f %f l " % (
                        float(l[0][0]),
                        float(l[0][1]),
                        float(l[1][0]),
                        float(l[1][1]),
                    )
                # stroke
                content += " S Q "

        # append to page
        page.append_to_content_stream(content)

    #
    # PUBLIC
    #

    def get_height(self) -> Decimal:
        """
        This function returns the height of this Shape
        :return:    the height
        """
        min_y: typing.Optional[Decimal] = None
        max_y: typing.Optional[Decimal] = None
        for cs in self._shapes:
            ys: typing.List[Decimal] = []
            if isinstance(cs, ConnectedShape):
                ys = [y for x, y in cs._points]
            if isinstance(cs, DisconnectedShape):
                ys = [src[1] for src, dst in cs._lines] + [
                    dst[1] for src, dst in cs._lines
                ]
            if min_y is None or min(ys) < min_y:
                min_y = min(ys)
            if max_y is None or max(ys) > max_y:
                max_y = max(ys)
        assert min_y is not None
        assert max_y is not None
        return max_y - min_y

    def get_width(self) -> Decimal:
        """
        This function returns the width of this Shape
        :return:    the width
        """
        min_x: typing.Optional[Decimal] = None
        max_x: typing.Optional[Decimal] = None
        for cs in self._shapes:
            xs: typing.List[Decimal] = []
            if isinstance(cs, ConnectedShape):
                xs = [x for x, y in cs._points]
            if isinstance(cs, DisconnectedShape):
                xs = [src[0] for src, dst in cs._lines] + [
                    dst[0] for src, dst in cs._lines
                ]
            if min_x is None or min(xs) < min_x:
                min_x = min(xs)
            if max_x is None or max(xs) > max_x:
                max_x = max(xs)
        assert min_x is not None
        assert max_x is not None
        return max_x - min_x

    def move_to(self, lower_left_x: Decimal, lower_left_y: Decimal) -> "Shapes":
        """
        This method translates this Shape so its lower left corner aligns with the given coordinates
        :param lower_left_x:    the desired lower left x-coordinate
        :param lower_left_y:    the desired lower left y-coordinate
        :return:    self
        """
        min_x: typing.Optional[Decimal] = None
        min_y: typing.Optional[Decimal] = None
        for cs in self._shapes:
            xs: typing.List[Decimal] = []
            ys: typing.List[Decimal] = []
            if isinstance(cs, ConnectedShape):
                xs = [x for x, y in cs._points]
                ys = [y for x, y in cs._points]
            if isinstance(cs, DisconnectedShape):
                xs = [src[0] for src, dst in cs._lines] + [
                    dst[0] for src, dst in cs._lines
                ]
                ys = [src[1] for src, dst in cs._lines] + [
                    dst[1] for src, dst in cs._lines
                ]
            if min_x is None or min(xs) < min_x:
                min_x = min(xs)
            if min_y is None or min(ys) < min_y:
                min_y = min(ys)

        # calculate delta
        assert min_x is not None
        assert min_y is not None
        delta_x = lower_left_x - min_x
        delta_y = lower_left_y - min_y

        # update (sub) shapes
        for cs in self._shapes:
            if isinstance(cs, ConnectedShape):
                cs._points = [(x[0] + delta_x, x[1] + delta_y) for x in cs._points]
            if isinstance(cs, DisconnectedShape):
                cs._lines = [
                    (
                        (x[0][0] + delta_x, x[0][1] + delta_y),
                        (x[1][0] + delta_x, x[1][1] + delta_y),
                    )
                    for x in cs._lines
                ]

        # return
        return self

    def scale_down(
        self,
        max_width: Decimal,
        max_height: Decimal,
        preserve_aspect_ratio: bool = True,
    ) -> "Shapes":
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
            for s in self._shapes:
                if isinstance(s, ConnectedShape):
                    s._points = [(x[0] * w_scale, x[1]) for x in s._points]
                if isinstance(s, DisconnectedShape):
                    s._lines = [
                        ((x[0][0] * w_scale, x[0][1]), (x[1][0] * w_scale, x[1][1]))
                        for x in s._lines
                    ]
        if h_scale < 1:
            for s in self._shapes:
                if isinstance(s, ConnectedShape):
                    s._points = [(x[0], x[1] * h_scale) for x in s._points]
                if isinstance(s, DisconnectedShape):
                    s._lines = [
                        ((x[0][0], x[0][1] * h_scale), (x[1][0], x[1][1] * h_scale))
                        for x in s._lines
                    ]
        return self

    def scale_up(
        self,
        max_width: Decimal,
        max_height: Decimal,
        preserve_aspect_ratio: bool = True,
    ) -> "Shapes":
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
            for s in self._shapes:
                if isinstance(s, ConnectedShape):
                    s._points = [(x[0] * w_scale, x[1]) for x in s._points]
                if isinstance(s, DisconnectedShape):
                    s._lines = [
                        ((x[0][0] * w_scale, x[0][1]), (x[1][0] * w_scale, x[1][1]))
                        for x in s._lines
                    ]
        if h_scale > 1:
            for s in self._shapes:
                if isinstance(s, ConnectedShape):
                    s._points = [(x[0], x[1] * h_scale) for x in s._points]
                if isinstance(s, DisconnectedShape):
                    s._lines = [
                        ((x[0][0], x[0][1] * h_scale), (x[1][0], x[1][1] * h_scale))
                        for x in s._lines
                    ]
        return self
