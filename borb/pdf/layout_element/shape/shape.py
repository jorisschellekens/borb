#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a drawable element composed of one or more polygons  or lines that can be rendered within a PDF layout.

This class supports a variety of geometric shapes, such as polygons, rectangles,
and custom line-based designs. It allows for detailed control over styling
attributes, including stroke color, fill color, line width, and positioning.

The `Shape` class is also responsible for defining the shape's boundaries and
supports transformations like scaling, rotating, and mirroring. Shapes are
commonly used for vector-based graphics in PDF documents.

It inherits from `LayoutElement`, allowing it to be integrated into a larger
document structure.
"""
import functools
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page

PolygonType: typing.TypeAlias = typing.List[typing.Tuple[float, float]]


class Shape(LayoutElement):
    """
    Represents a drawable element composed of one or more polygons  or lines that can be rendered within a PDF layout.

    This class supports a variety of geometric shapes, such as polygons, rectangles,
    and custom line-based designs. It allows for detailed control over styling
    attributes, including stroke color, fill color, line width, and positioning.

    The `Shape` class is also responsible for defining the shape's boundaries and
    supports transformations like scaling, rotating, and mirroring. Shapes are
    commonly used for vector-based graphics in PDF documents.

    It inherits from `LayoutElement`, allowing it to be integrated into a larger
    document structure.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        coordinates: typing.Union[PolygonType, typing.List[PolygonType]],
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        fill_color: typing.Optional[Color] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        line_width: int = 1,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new `Shape` object for rendering a line-art element in a PDF.

        This constructor allows customization of various layout and style properties
        for the shape, such as coordinates, margins, padding, borders, dash patterns,
        and alignment. These properties define the appearance and positioning of the
        shape within the PDF page.

        :param coordinates:            Coordinates defining the shape, as a single polygon
                                       or a list of polygons.
        :param background_color:       Optional background color for the shape's container.
        :param border_color:           Optional border color for the shape's container.
        :param border_dash_pattern:    Dash pattern used for the container's border lines.
        :param border_dash_phase:      Phase offset for the dash pattern in the container's borders.
        :param border_width_bottom:    Width of the bottom border of the container.
        :param border_width_left:      Width of the left border of the container.
        :param border_width_right:     Width of the right border of the container.
        :param border_width_top:       Width of the top border of the container.
        :param dash_pattern:           Dash pattern used for the shape's stroke.
        :param dash_phase:             Phase offset for the dash pattern in the shape's stroke.
        :param fill_color:             Optional fill color for the shape's interior.
        :param horizontal_alignment:   Horizontal alignment of the shape (default is LEFT).
        :param line_width:             Width of the shape's stroke.
        :param margin_bottom:          Space between the shape and the element below it.
        :param margin_left:            Space between the shape and the left page margin.
        :param margin_right:           Space between the shape and the right page margin.
        :param margin_top:             Space between the shape and the element above it.
        :param padding_bottom:         Padding inside the container at the bottom.
        :param padding_left:           Padding inside the container on the left side.
        :param padding_right:          Padding inside the container on the right side.
        :param padding_top:            Padding inside the container at the top.
        :param stroke_color:           Color of the shape's stroke (default is BLACK).
        :param vertical_alignment:     Vertical alignment of the shape (default is TOP).
        """
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_right=margin_right,
            margin_left=margin_left,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self.__coordinates: typing.Union[PolygonType, typing.List[PolygonType]] = (
            coordinates
        )
        self.__stroke_color: typing.Optional[Color] = stroke_color
        self.__fill_color: typing.Optional[Color] = fill_color
        self.__line_width: int = line_width
        self.__dash_pattern: typing.List[int] = dash_pattern
        self.__dash_phase: int = dash_phase

    #
    # PRIVATE
    #

    @staticmethod
    def __smooth_polygon(
        cs: typing.List[typing.Tuple[float, float]],
    ) -> typing.List[typing.Tuple[float, float]]:
        cs2 = [(x, y) for x, y in cs]
        for _ in range(0, 5):
            cs2 = Shape.__smooth_polygon_once(cs2)
        return cs2

    @staticmethod
    def __smooth_polygon_once(
        cs: typing.List[typing.Tuple[float, float]],
    ) -> typing.List[typing.Tuple[float, float]]:

        # IF the polygon does not contain at least 3 points
        # THEN do not attempt to interpolate
        if len(cs) == 0 or len(cs) == 1 or len(cs) == 2:
            return cs

        # IF the polygon is closed
        # THEN do not process the final point (as this would be a repeat of the first point)
        # AND add a copy of the first (output) point to the end
        if cs[0] == cs[-1]:
            cs_tmp: typing.List[typing.Tuple[float, float]] = cs[0:-1]
            d = [
                (
                    (
                        cs_tmp[i // 2 - 1][0] * 0.75 + cs_tmp[i // 2][0] * 0.25,
                        cs_tmp[i // 2 - 1][1] * 0.75 + cs_tmp[i // 2][1] * 0.25,
                    )
                    if i % 2 == 0
                    else (
                        cs_tmp[i // 2 - 1][0] * 0.25 + cs_tmp[i // 2][0] * 0.75,
                        cs_tmp[i // 2 - 1][1] * 0.25 + cs_tmp[i // 2][1] * 0.75,
                    )
                )
                for i in range(0, len(cs_tmp) * 2)
            ]
            d += [d[0]]
            return d

        # IF the polygon is open
        # THEN apply Chaikin's algorithm as is
        else:
            return [
                (
                    (
                        cs[i // 2 - 1][0] * 0.75 + cs[i // 2][0] * 0.25,
                        cs[i // 2 - 1][1] * 0.75 + cs[i // 2][1] * 0.25,
                    )
                    if i % 2 == 0
                    else (
                        cs[i // 2 - 1][0] * 0.25 + cs[i // 2][0] * 0.75,
                        cs[i // 2 - 1][1] * 0.25 + cs[i // 2][1] * 0.75,
                    )
                )
                for i in range(2, len(cs) * 2)
            ]

    #
    # PUBLIC
    #

    def get_polygons(self) -> typing.Union[PolygonType, typing.List[PolygonType]]:
        """
        Retrieve the polygons that define this Shape.

        This method returns the polygon(s) that make up the Shape. The returned value
        may be a single polygon or a list of polygons, depending on the Shape's
        structure.

        :return: The polygon(s) representing the Shape's geometry, either as a
                 single polygon or a list of polygons.
        """
        return self.__coordinates

    @functools.cache
    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        if len(self.__coordinates) == 0:
            return 0, 0

        # typing.List[PolygonType]
        min_x: float = math.inf
        min_y: float = math.inf
        max_x: float = -math.inf
        max_y: float = -math.inf
        if isinstance(self.__coordinates[0], list):
            # fmt: off
            min_x = min([min([x for x, _ in polygon]) for polygon in self.__coordinates])    # type: ignore[misc]
            max_x = max([max([x for x, _ in polygon]) for polygon in self.__coordinates])    # type: ignore[misc]
            min_y = min([min([y for _, y in polygon]) for polygon in self.__coordinates])    # type: ignore[misc]
            max_y = max([max([y for _, y in polygon]) for polygon in self.__coordinates])    # type: ignore[misc]
            # fmt: on
            return (
                int(math.ceil(max_x - min_x))
                + self.get_padding_right()
                + self.get_padding_left(),
                int(math.ceil(max_y - min_y))
                + self.get_padding_top()
                + self.get_padding_bottom(),
            )

        # PolygonType
        else:
            min_x = min([x for x, _ in self.__coordinates])  # type: ignore[assignment]
            max_x = max([x for x, _ in self.__coordinates])  # type: ignore[assignment]
            min_y = min([y for _, y in self.__coordinates])  # type: ignore[assignment]
            max_y = max([y for _, y in self.__coordinates])  # type: ignore[assignment]
            return (
                int(math.ceil(max_x - min_x))
                + self.get_padding_left()
                + self.get_padding_right(),
                int(math.ceil(max_y - min_y))
                + self.get_padding_top()
                + self.get_padding_bottom(),
            )

    def mirror_horizontally(self) -> "Shape":
        """
        Return a new Shape that represents a horizontal version of this Shape.

        :return: A new Shape object, horizontally adjusted.
        """
        # fmt: off
        return Shape(
            coordinates=(
                []  # type: ignore[arg-type]
                if len(self.__coordinates) == 0
                else (
                    [[(x, -y) for x, y in polygon] for polygon in self.__coordinates]   # type: ignore[misc]
                    if isinstance(self.__coordinates[0], list)
                    else [(x, -y) for x, y in self.__coordinates]                       # type: ignore[misc, operator]
                )
            ),
            stroke_color=self.__stroke_color,
            fill_color=self.__fill_color,
            line_width=self.__line_width,
            dash_pattern=self.__dash_pattern,
            dash_phase=self.__dash_phase,
            padding_top=self.get_padding_top(),
            padding_right=self.get_padding_right(),
            padding_left=self.get_padding_left(),
            padding_bottom=self.get_padding_bottom(),
        )
        # fmt: on

    def mirror_vertically(self) -> "Shape":
        """
        Mirror the current Shape vertically.

        :return: A new Shape object that is a vertical mirror image of this Shape.
        """
        # fmt: off
        return Shape(
            coordinates=(
                []  # type: ignore[arg-type]
                if len(self.__coordinates) == 0
                else (
                    [[(-x, y) for x, y in polygon] for polygon in self.__coordinates]   # type: ignore[misc]
                    if isinstance(self.__coordinates[0], list)
                    else [(-x, y) for x, y in self.__coordinates]                       # type: ignore[misc, operator]
                )
            ),
            stroke_color=self.__stroke_color,
            fill_color=self.__fill_color,
            line_width=self.__line_width,
            dash_pattern=self.__dash_pattern,
            dash_phase=self.__dash_phase,
            padding_top=self.get_padding_top(),
            padding_right=self.get_padding_right(),
            padding_left=self.get_padding_left(),
            padding_bottom=self.get_padding_bottom(),
        )
        # fmt: on

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        if len(self.__coordinates) == 0:
            return

        # calculate width and height
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

        # calculate where the background/borders need to be painted
        # fmt: off
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # BDC
        # fmt: off
        Shape._begin_marked_content_with_dictionary(page=page, structure_element_type='Figure')  # type: ignore[attr-defined]
        # fmt: on

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # leading newline (if needed)
        Shape._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # set fill color
        if self.__fill_color is not None:
            rgb_fill_color: RGBColor = self.__fill_color.to_rgb_color()
            page["Contents"]["DecodedBytes"] += (
                f"{round(rgb_fill_color.get_red() / 255, 7)} "
                f"{round(rgb_fill_color.get_green() / 255, 7)} "
                f"{round(rgb_fill_color.get_blue() / 255, 7)} rg\n"
            ).encode("latin1")

        # set stroke color
        if self.__stroke_color is not None:
            rgb_stroke_color: RGBColor = self.__stroke_color.to_rgb_color()
            page["Contents"]["DecodedBytes"] += (
                f"{round(rgb_stroke_color.get_red() / 255, 7)} "
                f"{round(rgb_stroke_color.get_green() / 255, 7)} "
                f"{round(rgb_stroke_color.get_blue() / 255, 7)} RG\n"
            ).encode("latin1")

        # set width
        page["Contents"]["DecodedBytes"] += f"{self.__line_width} w\n".encode("latin1")

        # set Line Cap Style
        page["Contents"]["DecodedBytes"] += f"1 J\n".encode("latin1")

        # set dash pattern
        page["Contents"][
            "DecodedBytes"
        ] += f"{self.__dash_pattern} {self.__dash_phase} d\n".encode("latin1")

        # draw/fill path
        min_x: float = math.inf
        min_y: float = math.inf
        x_delta: float = 0
        y_delta: float = 0
        if isinstance(self.__coordinates[0], list):
            # fmt: off
            min_x = min([min([x for x, _ in polygon]) for polygon in self.__coordinates])   # type: ignore[misc]
            min_y = min([min([y for _, y in polygon]) for polygon in self.__coordinates])   # type: ignore[misc]
            x_delta = -min_x + background_x + self.get_padding_left()
            y_delta = -min_y + background_y + self.get_padding_bottom()
            # fmt: on
        else:
            # fmt: off
            min_x = min([x for x, _ in self.__coordinates])                     # type: ignore[assignment]
            min_y = min([y for _, y in self.__coordinates])                     # type: ignore[assignment]
            x_delta = -min_x + background_x + self.get_padding_left()
            y_delta = -min_y + background_y + self.get_padding_bottom()
            # fmt: on

        if isinstance(self.__coordinates[0], list):
            for polygon in self.__coordinates:
                # fmt: off
                page["Contents"]["DecodedBytes"] += f"{round(polygon[0][0] + x_delta, 7)} {round(polygon[0][1] + y_delta, 7)} m\n".encode('latin1')    # type: ignore[index]
                for x, y in polygon[1:]:                                                                            # type: ignore[misc]
                    page["Contents"]["DecodedBytes"] += f"{round(x + x_delta, 7)} {round(y + y_delta, 7)} l\n".encode('latin1')
                if self.__fill_color is not None and self.__stroke_color is not None:
                    page["Contents"]["DecodedBytes"] += b"B\n"
                elif self.__fill_color is not None:
                    page["Contents"]["DecodedBytes"] += b"f\n"
                elif self.__stroke_color is not None:
                    page["Contents"]["DecodedBytes"] += b"S\n"
                # fmt: on
        else:
            # fmt: off
            page["Contents"]["DecodedBytes"] += f"{round(self.__coordinates[0][0] + x_delta, 7)} {round(self.__coordinates[0][1] + y_delta, 7)} m\n".encode('latin1')
            for x, y in self.__coordinates[1:]:
                page["Contents"]["DecodedBytes"] += f"{round(x + x_delta, 7)} {round(y + y_delta, 7)} l\n".encode('latin1')    # type: ignore[operator]
            if self.__fill_color is not None and self.__stroke_color is not None:
                page["Contents"]["DecodedBytes"] += b"B\n"
            elif self.__fill_color is not None:
                page["Contents"]["DecodedBytes"] += b"f\n"
            elif self.__stroke_color is not None:
                page["Contents"]["DecodedBytes"] += b"S\n"
            # fmt: on

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"

        # EMC
        Shape._end_marked_content(page=page)  # type: ignore[attr-defined]

    def rotate(self, angle_in_degrees: float) -> "Shape":
        """
        Rotate the Shape clockwise by the specified angle in degrees.

        :param angle_in_degrees: The angle in degrees by which to rotate the Shape.
        :return: A new Shape object, rotated by the specified angle.
        """
        angle_in_radians: float = math.radians(angle_in_degrees)
        a: float = math.cos(angle_in_radians)
        b: float = -math.sin(angle_in_radians)
        c: float = math.sin(angle_in_radians)
        d: float = math.cos(angle_in_radians)
        # fmt: off
        return Shape(
            coordinates=(
                []
                if len(self.__coordinates) == 0
                else (
                    [[(a * x + c * y, b * x + d * y) for x, y in polygon] for polygon in self.__coordinates] # type: ignore[misc]
                    if isinstance(self.__coordinates[0], list)
                    else [(a * x + c * y, b * x + d * y) for x, y in self.__coordinates] # type: ignore[misc, operator]
                )
            ),
            stroke_color=self.__stroke_color,
            fill_color=self.__fill_color,
            line_width=self.__line_width,
            dash_pattern=self.__dash_pattern,
            dash_phase=self.__dash_phase,
            padding_top=self.get_padding_top(),
            padding_right=self.get_padding_right(),
            padding_left=self.get_padding_left(),
            padding_bottom=self.get_padding_bottom(),
        )
        # fmt: on

    def scale_by_factor(self, x_factor: float = 1, y_factor: float = 1) -> "Shape":
        """
        Scale this Shape by the given factors along the x and y axes.

        This method scales the Shape horizontally by `x_factor` and vertically by `y_factor`.
        The result is a new Shape object that has been resized according to the provided factors.

        :param x_factor: The scale factor for the x-axis.
        :param y_factor: The scale factor for the y-axis.
        :return: A new Shape object scaled by the given factors.
        """
        assert x_factor != 0, "The x_factor must be a non-zero number."
        assert y_factor != 0, "The y_factor must be a non-zero number."
        # fmt: off
        return Shape(
            coordinates=(
                []  # type: ignore[arg-type]
                if len(self.__coordinates) == 0
                else (
                    [[(x * x_factor, y * y_factor) for x, y in polygon] for polygon in self.__coordinates]  # type: ignore[misc]
                    if isinstance(self.__coordinates[0], list)
                    else [(x * x_factor, y * y_factor) for x, y in self.__coordinates]  # type: ignore[misc, operator]
                )
            ),
            stroke_color=self.__stroke_color,
            fill_color=self.__fill_color,
            line_width=self.__line_width,
            dash_pattern=self.__dash_pattern,
            dash_phase=self.__dash_phase,
            padding_top=self.get_padding_top(),
            padding_right=self.get_padding_right(),
            padding_left=self.get_padding_left(),
            padding_bottom=self.get_padding_bottom(),
        )
        # fmt: on

    def scale_to_fit(self, size: typing.Tuple[int, int]) -> "Shape":
        """
        Scale this Shape proportionally to fit within the given (width, height) dimensions.

        The aspect ratio is preserved. The resulting Shape will not exceed the specified
        size in either width or height.

        :param size: A tuple (width, height) representing the maximum allowed dimensions.
        :return: A new Shape instance scaled to fit within the given bounds.
        """
        width, height = size
        assert width >= 0
        assert height >= 0

        w_avail: int = width - self.get_padding_left() - self.get_padding_right()
        h_avail: int = height - self.get_padding_top() - self.get_padding_bottom()

        min_x: float = math.inf
        min_y: float = math.inf
        max_x: float = -math.inf
        max_y: float = -math.inf
        w: int = 0
        h: int = 0
        if isinstance(self.__coordinates[0], list):
            # fmt: off
            min_x = min([min([x for x, _ in polygon]) for polygon in self.__coordinates])       # type: ignore[misc]
            max_x = max([max([x for x, _ in polygon]) for polygon in self.__coordinates])       # type: ignore[misc]
            min_y = min([min([y for _, y in polygon]) for polygon in self.__coordinates])       # type: ignore[misc]
            max_y = max([max([y for _, y in polygon]) for polygon in self.__coordinates])       # type: ignore[misc]
            # fmt: on
            w = int(math.ceil(max_x - min_x))
            h = int(math.ceil(max_y - min_y))

        # PolygonType
        else:
            min_x = min([x for x, _ in self.__coordinates])  # type: ignore[assignment]
            max_x = max([x for x, _ in self.__coordinates])  # type: ignore[assignment]
            min_y = min([y for _, y in self.__coordinates])  # type: ignore[assignment]
            max_y = max([y for _, y in self.__coordinates])  # type: ignore[assignment]
            w = int(math.ceil(max_x - min_x))
            h = int(math.ceil(max_y - min_y))

        w_ratio: float = w_avail / w
        h_ratio: float = h_avail / h
        ratio: float = min(w_ratio, h_ratio)

        # apply
        return self.scale_by_factor(x_factor=ratio, y_factor=ratio)

    def smooth(self) -> "Shape":
        """
        Apply Chaikin's algorithm to smooth the polygons within this Shape.

        This method processes each polygon in the current Shape using Chaikin's corner-cutting
        algorithm, which reduces sharp angles and smooths the curves. The result is a new
        Shape object where the polygons have a more refined and smoother appearance.

        :return: A new Shape object with smoothed polygons.
        """
        # fmt: off
        return Shape(
            coordinates=(
                []
                if len(self.__coordinates) == 0
                else (
                    [Shape.__smooth_polygon(polygon) for polygon in self.__coordinates]     # type: ignore[arg-type]
                    if isinstance(self.__coordinates[0], list)
                    else Shape.__smooth_polygon(self.__coordinates)                         # type: ignore[arg-type]
                )
            ),
            stroke_color=self.__stroke_color,
            fill_color=self.__fill_color,
            line_width=self.__line_width,
            dash_pattern=self.__dash_pattern,
            dash_phase=self.__dash_phase,
            padding_top=self.get_padding_top(),
            padding_right=self.get_padding_right(),
            padding_left=self.get_padding_left(),
            padding_bottom=self.get_padding_bottom(),
        )
        # fmt: on
