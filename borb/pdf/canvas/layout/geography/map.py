#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A world map is a map of most or all of the surface of Earth. World maps, because of their scale,
must deal with the problem of projection.
Maps rendered in two dimensions by necessity distort the display of the three-dimensional surface of the Earth.
While this is true of any map, these distortions reach extremes in a world map.
Many techniques have been developed to present world maps that address diverse technical and aesthetic goals.
"""
import json
import typing
from decimal import Decimal
import pathlib

from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.shape.shapes import Shapes


class Map(Shapes):
    """
    A world map is a map of most or all of the surface of Earth. World maps, because of their scale,
    must deal with the problem of projection.
    Maps rendered in two dimensions by necessity distort the display of the three-dimensional surface of the Earth.
    While this is true of any map, these distortions reach extremes in a world map.
    Many techniques have been developed to present world maps that address diverse technical and aesthetic goals.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        geojson_file: pathlib.Path,
        name_key: str,
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
        line_width: Decimal = Decimal(1),
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

        # keep track of all countries
        # fmt: off
        self._iso3_code_to_shapes: typing.Dict[str, typing.List[ConnectedShape]] = {}
        # fmt: on

        # read map
        with open(geojson_file, "r") as json_file_handle:
            geo_json_data = json.loads(json_file_handle.read())
            for feature_dict in geo_json_data["features"]:
                iso3_key: str = feature_dict["properties"].get(name_key, None)
                self._iso3_code_to_shapes[iso3_key] = []
                for polygon in feature_dict["geometry"]["coordinates"]:
                    if (
                        isinstance(polygon, typing.List)
                        and isinstance(polygon[0], typing.List)
                        and isinstance(polygon[0][0], typing.List)
                    ):
                        polygon = polygon[0]
                    self._iso3_code_to_shapes[iso3_key].append(
                        ConnectedShape(
                            [(Decimal(x), Decimal(y)) for x, y in polygon],
                            stroke_color=stroke_color,
                            fill_color=fill_color,
                            line_width=line_width,
                        )
                    )

        # all shapes
        all_shapes: typing.List[typing.Union[ConnectedShape, DisconnectedShape]] = []
        for css in self._iso3_code_to_shapes.values():
            all_shapes.extend(css)

        # init
        super(Map, self).__init__(
            shapes=all_shapes,
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

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def pop(self, key: str) -> "Map":
        """
        This function removes a key (associated with one or multiple ConnectedShape or DisconnectedShape objects)
        :param key:     the key to be removed
        :return:        self
        """
        shapes_to_remove: typing.Optional[
            typing.List[ConnectedShape]
        ] = self._iso3_code_to_shapes.get(key, None)
        if shapes_to_remove is not None:
            self._iso3_code_to_shapes.pop(key)
            self._shapes = [x for x in self._shapes if x not in shapes_to_remove]
        return self

    def set_fill_color(
        self,
        fill_color: Color,
        key: typing.Optional[str] = None,
    ) -> "Map":
        """
        This function sets the fill Color of all countries, or a specific country (specified by its ISO3 code)
        :param fill_color:          the fill Color
        :param key:                 an ISO3 country code, or None
        :return:                    self
        """
        if key is None:
            for _, css in self._iso3_code_to_shapes.items():
                for cs in css:
                    cs._fill_color = fill_color
        else:
            for cs in self._iso3_code_to_shapes[key]:
                cs._fill_color = fill_color

        return self

    def set_line_width(
        self,
        line_width: Decimal,
        key: typing.Optional[str] = None,
    ) -> "Map":
        """
        This function sets the line width of all countries, or a specific country (specified by its ISO3 code)
        :param line_width:          the line width
        :param key:                 an ISO3 country code, or None
        :return:                    self
        """
        if key is None:
            for _, css in self._iso3_code_to_shapes.items():
                for cs in css:
                    cs._line_width = line_width
        else:
            for cs in self._iso3_code_to_shapes[key]:
                cs._line_width = line_width
        return self

    def set_stroke_color(
        self,
        stroke_color: Color,
        key: typing.Optional[str] = None,
    ) -> "Map":
        """
        This function sets the stroke Color of all countries, or a specific country (specified by its ISO3 code)
        :param stroke_color:        the stroke Color
        :param key:                 an ISO3 country code, or None
        :return:                    self
        """
        if key is None:
            for _, css in self._iso3_code_to_shapes.items():
                for cs in css:
                    cs._stroke_color = stroke_color
        else:
            for cs in self._iso3_code_to_shapes[key]:
                cs._stroke_color = stroke_color
        return self
