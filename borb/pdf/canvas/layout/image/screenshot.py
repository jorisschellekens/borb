#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A screenshot (also known as screen capture or screen grab) is a digital image that shows the contents of a computer display.
A screenshot is created by the operating system or software running on the device powering the display.
"""
import typing
from decimal import Decimal

from PIL import ImageGrab

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment


class ScreenShot(Image):
    """
    A screenshot (also known as screen capture or screen grab) is a digital image that shows the contents of a computer display.
    A screenshot is created by the operating system or software running on the device powering the display.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        all_screens: bool = False,
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
        bounding_box: typing.Optional[Rectangle] = None,
        height: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        include_layered_windows: bool = False,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
        width: typing.Optional[Decimal] = None,
        x_display: typing.Optional[str] = None,
    ):
        super().__init__(
            image=ImageGrab.grab(
                bbox=None
                if bounding_box is None
                else (
                    int(bounding_box.get_x()),
                    int(bounding_box.get_y()),
                    int(bounding_box.get_width()),
                    int(bounding_box.get_height()),
                ),
                include_layered_windows=include_layered_windows,
                all_screens=all_screens,
                xdisplay=x_display,
            ),
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
            height=height,
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
            width=width,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
