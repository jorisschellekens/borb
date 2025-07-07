#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A generic class representing a map as a drawable shape in a PDF document.

The Map class provides functionality to render geographic regions (such as countries or states) within a PDF.
It retrieves geographic data from a compressed geo-JSON file and allows customization of regions by specifying
fill and stroke colors for each one. The Map class can be specialized to represent different parts of the world,
such as Europe or the entire globe.

Use this class to generate maps, customize region appearances, and integrate geographic shapes into a PDF.
"""
import functools
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.page import Page

PolygonType: typing.TypeAlias = typing.List[typing.Tuple[float, float]]
PolygonsType: typing.TypeAlias = typing.List[PolygonType]


class Map(Shape):
    """
    A generic class representing a map as a drawable shape in a PDF document.

    The Map class provides functionality to render geographic regions (such as countries or states) within a PDF.
    It retrieves geographic data from a compressed geo-JSON file and allows customization of regions by specifying
    fill and stroke colors for each one. The Map class can be specialized to represent different parts of the world,
    such as Europe or the entire globe.

    Use this class to generate maps, customize region appearances, and integrate geographic shapes into a PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        geo_json: typing.Dict,
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
        Initialize a Map object that represents geographical shapes and lines.

        This constructor takes in a GeoJSON dictionary to define the shapes and lines
        to be rendered in the map. It also allows for customization of various
        visual properties, such as colors, borders, and alignment.

        :param geo_json: A dictionary containing GeoJSON data that defines the map's features.
        :param background_color: The background color of the map (default is None).
        :param border_color: The color of the border surrounding the map (default is None).
        :param border_dash_pattern: A list defining the dash pattern for the border (default is an empty list).
        :param border_dash_phase: The phase for the dashed border (default is 0).
        :param border_width_bottom: The width of the bottom border (default is 0).
        :param border_width_left: The width of the left border (default is 0).
        :param border_width_right: The width of the right border (default is 0).
        :param border_width_top: The width of the top border (default is 0).
        :param dash_pattern: A list defining the dash pattern for map features (default is an empty list).
        :param dash_phase: The phase for dashed map features (default is 0).
        :param fill_color: The fill color for map regions (default is None).
        :param horizontal_alignment: The horizontal alignment of the map (default is left).
        :param line_width: The line width for drawing map features (default is 0.1).
        :param margin_bottom: The bottom margin around the map (default is 0).
        :param margin_left: The left margin around the map (default is 0).
        :param margin_right: The right margin around the map (default is 0).
        :param margin_top: The top margin around the map (default is 0).
        :param padding_bottom: The bottom padding inside the map (default is 0).
        :param padding_left: The left padding inside the map (default is 0).
        :param padding_right: The right padding inside the map (default is 0).
        :param padding_top: The top padding inside the map (default is 0).
        :param stroke_color: The stroke color for map features (default is black).
        :param vertical_alignment: The vertical alignment of the map (default is top).
        """
        super().__init__(
            coordinates=[],
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            dash_pattern=dash_pattern,
            dash_phase=dash_phase,
            fill_color=fill_color,
            horizontal_alignment=horizontal_alignment,
            line_width=line_width,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            stroke_color=stroke_color,
            vertical_alignment=vertical_alignment,
        )

        # build synonyms
        self.__synonyms: typing.Dict[str, str] = {}
        for d in geo_json["features"]:
            base_name: typing.Optional[str] = d["properties"].get("name_en", None) or d[
                "properties"
            ].get("name", None)
            if base_name is None:
                continue
            for k, v in d["properties"].items():
                if not k.startswith("name_"):
                    continue
                if v is None:
                    continue
                self.__synonyms[v] = base_name

        # shapes
        self.__name_to_shape: typing.Dict[str, PolygonsType] = {
            d["properties"]["name"]: Map.__convert_geometry_to_polygons_type(
                d["geometry"]
            )
            for d in geo_json["features"]
        }

        # stroke color
        self.__name_to_stroke_color: typing.Dict[str, Color] = {}

        # fill color
        self.__name_to_fill_color: typing.Dict[str, Color] = {}

        # scale
        self.__scale_to_fit_in_place(size=(100, 100))

    #
    # PRIVATE
    #

    @staticmethod
    def __convert_geometry_to_polygons_type(d) -> PolygonsType:
        if d.get("type", "") == "Polygon":
            return [[(y[0], y[1]) for y in x] for x in d["coordinates"]]
        if d.get("type", "") == "MultiPolygon":
            t = []
            for x in d["coordinates"]:
                for y in x:
                    t += [[(z[0], z[1]) for z in y]]
            return t
        return []

    def __scale_to_fit_in_place(self, size: typing.Tuple[int, int]) -> None:
        w_avail: int = size[0] - self.get_padding_left() - self.get_padding_right()
        h_avail: int = size[1] - self.get_padding_top() - self.get_padding_bottom()

        min_x: float = math.inf
        min_y: float = math.inf
        max_x: float = -math.inf
        max_y: float = -math.inf
        for polygons in self.__name_to_shape.values():
            for polygon in polygons:
                min_x = min(min_x, min([x for x, _ in polygon]))
                min_y = min(min_y, min([y for _, y in polygon]))
                max_x = max(max_x, max([x for x, _ in polygon]))
                max_y = max(max_y, max([y for _, y in polygon]))

        # calculate actual width/height
        w = int(math.ceil(max_x - min_x))
        h = int(math.ceil(max_y - min_y))

        # calculate scaling factor(s)
        w_ratio: float = w_avail / w
        h_ratio: float = h_avail / h
        ratio: float = min(w_ratio, h_ratio)

        # apply ratio
        self.__name_to_shape = {
            name: [
                [(point[0] * ratio, point[1] * ratio) for point in polygon]
                for polygon in polygons
            ]
            for name, polygons in self.__name_to_shape.items()
        }

    #
    # PUBLIC
    #

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
        min_x: float = math.inf
        min_y: float = math.inf
        max_x: float = -math.inf
        max_y: float = -math.inf
        for polygons in self.__name_to_shape.values():
            for polygon in polygons:
                min_x = min(min_x, min([x for x, _ in polygon]))
                min_y = min(min_y, min([y for _, y in polygon]))
                max_x = max(max_x, max([x for x, _ in polygon]))
                max_y = max(max_y, max([y for _, y in polygon]))

        return (
            int(math.ceil(max_x - min_x))
            + self.get_padding_right()
            + self.get_padding_left(),
            int(math.ceil(max_y - min_y))
            + self.get_padding_top()
            + self.get_padding_bottom(),
        )

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
        # calculate width and height
        w, h = self.get_size(available_space=(2**64, 2**64))

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

        min_x: float = math.inf
        min_y: float = math.inf
        x_delta: float = 0
        y_delta: float = 0
        for polygons in self.__name_to_shape.values():
            for polygon in polygons:
                min_x = min(min_x, min([x for x, _ in polygon]))
                min_y = min(min_y, min([y for _, y in polygon]))
                x_delta = -min_x + background_x + self.get_padding_left()
                y_delta = -min_y + background_y + self.get_padding_bottom()
            # fmt: on

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # leading newline (if needed)
        Map._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # set width
        page["Contents"]["DecodedBytes"] += f"{self._Shape__line_width} w\n".encode("latin1")  # type: ignore[attr-defined]

        # set Line Cap Style
        page["Contents"]["DecodedBytes"] += f"1 J\n".encode("latin1")

        # set dash pattern
        # fmt: off
        page["Contents"]["DecodedBytes"] += f"{self._Shape__dash_pattern} {self._Shape__dash_phase} d\n".encode('latin1')  # type: ignore[attr-defined]
        # fmt: on

        # draw each shape
        for name, polygons in self.__name_to_shape.items():

            # set fill color
            # fmt: off
            fill_color: typing.Optional[Color] = self.__name_to_fill_color.get(name, self._Shape__fill_color) # type: ignore[attr-defined]
            if fill_color is not None:
                rgb_fill_color: RGBColor = fill_color.to_rgb_color()
                page["Contents"]["DecodedBytes"] += (
                    f"{round(rgb_fill_color.get_red() / 255, 7)} "
                    f"{round(rgb_fill_color.get_green() / 255, 7)} "
                    f"{round(rgb_fill_color.get_blue() / 255, 7)} rg\n"
                ).encode('latin1')
            # fmt: on

            # set stroke color
            # fmt: off
            stroke_color: typing.Optional[Color] = self.__name_to_stroke_color.get(name, self._Shape__stroke_color) # type: ignore[attr-defined]
            if stroke_color is not None:
                rgb_stroke_color: RGBColor = stroke_color.to_rgb_color()
                page["Contents"]["DecodedBytes"] += (
                    f"{round(rgb_stroke_color.get_red() / 255, 7)} "
                    f"{round(rgb_stroke_color.get_green() / 255, 7)} "
                    f"{round(rgb_stroke_color.get_blue() / 255, 7)} RG\n"
                ).encode('latin1')
            # fmt: on

            # stroke shape
            for polygon in polygons:
                page["Contents"]["DecodedBytes"] += f"{polygon[0][0] + x_delta} {polygon[0][1] + y_delta} m\n".encode("latin1")  # type: ignore[index]
                for x, y in polygon[1:]:  # type: ignore[misc]
                    # fmt: off
                    page["Contents"]["DecodedBytes"] += f"{x + x_delta} {y + y_delta} l\n".encode('latin1')
                    # fmt: on
                if fill_color is not None and stroke_color is not None:
                    page["Contents"]["DecodedBytes"] += b"B\n"
                elif fill_color is not None:
                    page["Contents"]["DecodedBytes"] += b"f\n"
                elif stroke_color is not None:
                    page["Contents"]["DecodedBytes"] += b"S\n"

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"

    def rotate(self, angle_in_degrees: float) -> "Map":
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

        # rotate
        import copy

        out: Map = copy.deepcopy(self)
        for name, polygons in out.__name_to_shape.items():
            t = []
            for polygon in polygons:
                t += [[(a * x + c * y, b * x + d * y) for x, y in polygon]]
            out.__name_to_shape[name] = t

        # return
        return out

    def scale_by_factor(self, x_factor: float = 1, y_factor: float = 1) -> "Shape":
        """
        Scale this Shape by the given factors along the x and y axes.

        This method scales the Shape horizontally by `x_factor` and vertically by `y_factor`.
        The result is a new Shape object that has been resized according to the provided factors.

        :param x_factor: The scale factor for the x-axis.
        :param y_factor: The scale factor for the y-axis.
        :return: A new Shape object scaled by the given factors.
        """
        assert x_factor != 0
        assert y_factor != 0

        # scale
        import copy

        out: Map = copy.deepcopy(self)
        for name, polygons in out.__name_to_shape.items():
            t = []
            for polygon in polygons:
                t += [[(x * x_factor, y * y_factor) for x, y in polygon]]
            out.__name_to_shape[name] = t

        # return
        return out

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
        for polygons in self.__name_to_shape.values():
            for polygon in polygons:
                min_x = min(min_x, min([x for x, _ in polygon]))
                min_y = min(min_y, min([y for _, y in polygon]))
                max_x = max(max_x, max([x for x, _ in polygon]))
                max_y = max(max_y, max([y for _, y in polygon]))

        w = int(math.ceil(max_x - min_x))
        h = int(math.ceil(max_y - min_y))

        w_ratio: float = w_avail / w
        h_ratio: float = h_avail / h
        ratio: float = min(w_ratio, h_ratio)

        # apply
        return self.scale_by_factor(x_factor=ratio, y_factor=ratio)

    def set_fill_color(self, fill_color: Color, name: str) -> "Map":
        """
        Set the fill color for a specific region on the map.

        This method allows you to specify a region by its name and assign a fill color to it.
        For example, you can color France in yellow while keeping the rest of the map in gray.
        This is useful for highlighting specific countries, states, or regions on the map.

        :param fill_color:  The color to fill the specified region with.
        :param name:        The name of the region (e.g., country, state, etc.) to be colored.
        :return:            Returns the modified Map instance, allowing for method chaining.
        """
        if name not in self.__name_to_shape:
            name = self.__synonyms.get(name, name)
        self.__name_to_fill_color[name] = fill_color
        return self

    def set_stroke_color(self, name: str, stroke_color: Color) -> "Map":
        """
        Set the stroke (border) color for a specific region on the map.

        This method allows you to specify a region by its name and assign a stroke color to its border.
        For instance, you can set the border color of France to blue while keeping the rest of the map's
        borders in a different color or unchanged. This is useful for highlighting specific regions.

        :param name:            The name of the region (e.g., country, state, etc.) whose border color will be set.
        :param stroke_color:    The color to apply to the border of the specified region.
        :return:                Returns the modified Map instance, allowing for method chaining.
        """
        if name not in self.__name_to_shape:
            name = self.__synonyms.get(name, name)
        self.__name_to_stroke_color[name] = stroke_color
        return self

    def smooth(self) -> "Shape":
        """
        Apply Chaikin's algorithm to smooth the polygons within this Shape.

        This method processes each polygon in the current Shape using Chaikin's corner-cutting
        algorithm, which reduces sharp angles and smooths the curves. The result is a new
        Shape object where the polygons have a more refined and smoother appearance.

        :return: A new Shape object with smoothed polygons.
        """
        # smooth
        import copy

        out: Map = copy.deepcopy(self)
        for name, polygons in out.__name_to_shape.items():
            t = []
            for polygon in polygons:
                t += [Shape._Shape__smooth_polygon(polygon)]  # type: ignore[attr-defined]
            out.__name_to_shape[name] = t

        # return
        return out
