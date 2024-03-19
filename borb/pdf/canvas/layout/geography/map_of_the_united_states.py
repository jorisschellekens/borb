#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A world map is a map of most or all of the surface of Earth. World maps, because of their scale,
must deal with the problem of projection.
Maps rendered in two dimensions by necessity distort the display of the three-dimensional surface of the Earth.
While this is true of any map, these distortions reach extremes in a world map.
Many techniques have been developed to present world maps that address diverse technical and aesthetic goals.
"""
import typing
from decimal import Decimal
import pathlib

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.geography.map import Map
from borb.pdf.canvas.layout.layout_element import Alignment


class MapOfTheUnitedStates(Map):
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
        # init
        super(MapOfTheUnitedStates, self).__init__(
            geojson_file=(pathlib.Path(__file__).parent / "geojson")
            / "map_of_the_united_states.geojson",
            name_key="name",
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
