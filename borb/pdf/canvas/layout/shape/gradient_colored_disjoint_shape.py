#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a generic disjoint shape (specified by a List of lines),
that will be colored according to a gradient.
It has convenience methods to calculate width and height, perform scaling, etc
"""
import enum
import math
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HSVColor, RGBColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.shape.disjoint_shape import DisjointShape
from borb.pdf.page.page import Page


class GradientColoredDisjointShape(DisjointShape):
    """
    This class represents a generic disjoint shape (specified by a List of lines),
    that will be colored according to a gradient.
    It has convenience methods to calculate width and height, perform scaling, etc
    """

    class GradientType(enum.Enum):
        """
        This enumeration represents the type
        of gradient that will be applied to this DisjointShape.
        """

        DIAGONAL = 1
        HORIZONTAL = 2
        RADIAL = 3
        VERTICAL = 4

    def __init__(
        self,
        shape: DisjointShape,
        from_color: Color,
        to_color: Color,
        gradient_type: GradientType = GradientType.RADIAL,
    ):
        super(GradientColoredDisjointShape, self).__init__(
            shape._lines,
            shape._stroke_color,
            shape._line_width,
            shape._horizontal_alignment,
            shape._vertical_alignment,
            shape._preserve_aspect_ratio,
        )
        self._from_color: Color = from_color
        self._to_color: Color = to_color
        self._gradient_type: GradientColoredDisjointShape.GradientType = gradient_type

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
        content = "q %d w " % (self._line_width,)
        min_x: Decimal = min([min(l[0][0], l[1][0]) for l in self._lines])
        min_y: Decimal = min([min(l[0][1], l[1][1]) for l in self._lines])
        max_x: Decimal = max([min(l[0][0], l[1][0]) for l in self._lines])
        max_y: Decimal = max([max(l[0][1], l[1][1]) for l in self._lines])

        # we need to calculate the norm (the max distance between a line and the origin of the gradient)
        n: Decimal = Decimal(1)

        # DIAGONAL
        if self._gradient_type == GradientColoredDisjointShape.GradientType.DIAGONAL:
            n = math.sqrt((min_x - max_x) ** 2 + (min_y - max_y) ** 2)

        # HORIZONTAL
        if self._gradient_type == GradientColoredDisjointShape.GradientType.HORIZONTAL:
            n = max_x - min_x

        # RADIAL
        if self._gradient_type == GradientColoredDisjointShape.GradientType.RADIAL:
            mid_x = (max_x - min_x) / 2 + min_x
            mid_y = (max_y - min_y) / 2 + min_y
            n = max(
                [
                    math.sqrt((l[0][0] - mid_x) ** 2 + (l[0][1] - mid_y) ** 2)
                    for l in self._lines
                ]
            )

        # VERTICAL
        if self._gradient_type == GradientColoredDisjointShape.GradientType.VERTICAL:
            n = max_y - min_y

        # convert to Decimal to be sure
        n = Decimal(n)

        # calculate colors as HSV
        start_color: HSVColor = HSVColor.from_rgb(self._from_color.to_rgb())
        end_color: HSVColor = HSVColor.from_rgb(self._to_color.to_rgb())

        # now we can draw each line
        for l in self._lines:
            d: Decimal = Decimal(0)
            if (
                self._gradient_type
                == GradientColoredDisjointShape.GradientType.DIAGONAL
            ):
                d = math.sqrt((l[0][0] - min_x) ** 2 + (l[0][1] - min_y) ** 2)
            if (
                self._gradient_type
                == GradientColoredDisjointShape.GradientType.HORIZONTAL
            ):
                d = l[0][0] - min_x
            if self._gradient_type == GradientColoredDisjointShape.GradientType.RADIAL:
                d = math.sqrt((l[0][0] - mid_x) ** 2 + (l[0][1] - mid_y) ** 2)
            if (
                self._gradient_type
                == GradientColoredDisjointShape.GradientType.VERTICAL
            ):
                d = l[0][1] - min_y
            d = Decimal(d)

            # calculate color based on the distance between this line and the origin of the gradient
            h = start_color.hue + (end_color.hue - start_color.hue) * (d / n)
            s = start_color.saturation + (
                end_color.saturation - start_color.saturation
            ) * (d / n)
            v = start_color.value + (end_color.value - start_color.value) * (d / n)

            # convert to RGB
            stroke_color: RGBColor = HSVColor(h, s, v).to_rgb()
            r: Decimal = Decimal(stroke_color.red)
            g: Decimal = Decimal(stroke_color.green)
            b: Decimal = Decimal(stroke_color.blue)

            # write content
            content += "%f %f %f RG %f %f m %f %f l S " % (
                r,
                g,
                b,
                l[0][0],
                l[0][1],
                l[1][0],
                l[1][1],
            )

        # stroke
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
