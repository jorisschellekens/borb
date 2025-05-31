#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a screenshot that can be inserted into a PDF document.

The `Screenshot` class allows users to capture and insert a screenshot into a PDF. It inherits
from the `Image` class, which provides core functionality for handling images in PDF layouts.
The screenshot can be captured directly from the user's screen and then processed like any
other image object.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class Screenshot(Image):
    """
    Represents a screenshot that can be inserted into a PDF document.

    The `Screenshot` class allows users to capture and insert a screenshot into a PDF. It inherits
    from the `Image` class, which provides core functionality for handling images in PDF layouts.
    The screenshot can be captured directly from the user's screen and then processed like any
    other image object.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        all_screens: bool = False,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        bounding_box: typing.Optional[typing.Tuple[int, int, int, int]] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        include_layered_windows: bool = False,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Optional[typing.Tuple[int, int]] = None,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
        xdisplay: typing.Optional[str] = None,
    ):
        """
        Initialize a Screenshot object.

        The `Screenshot` class is designed to capture screenshots with customizable options,
        including the ability to capture all screens, specify background and border colors,
        and define the size and alignment of the screenshot.

        :param all_screens:             If True, capture screenshots from all connected screens. Defaults to False.
        :param background_color:        The background color of the screenshot. Defaults to None.
        :param border_color:            The color of the border around the screenshot. Defaults to None.
        :param border_dash_pattern:     A list defining the dash pattern for the border. Defaults to an empty list.
        :param border_dash_phase:       The phase of the dash pattern. Defaults to 0.
        :param border_width_bottom:     Width of the bottom border in pixels. Defaults to 0.
        :param border_width_left:       Width of the left border in pixels. Defaults to 0.
        :param border_width_right:      Width of the right border in pixels. Defaults to 0.
        :param border_width_top:        Width of the top border in pixels. Defaults to 0.
        :param bounding_box:            A tuple defining the bounding box of the screenshot in the form (x1, y1, x2, y2). Defaults to None.
        :param horizontal_alignment:    Horizontal alignment of the screenshot. Defaults to LayoutElement.HorizontalAlignment.LEFT.
        :param include_layered_windows: If True, include layered (translucent) windows in the screenshot. Defaults to False.
        :param margin_bottom:           Bottom margin in pixels. Defaults to 0.
        :param margin_left:             Left margin in pixels. Defaults to 0.
        :param margin_right:            Right margin in pixels. Defaults to 0.
        :param margin_top:              Top margin in pixels. Defaults to 0.
        :param padding_bottom:          Bottom padding in pixels. Defaults to 0.
        :param padding_left:            Left padding in pixels. Defaults to 0.
        :param padding_right:           Right padding in pixels. Defaults to 0.
        :param padding_top:             Top padding in pixels. Defaults to 0.
        :param size:                    Desired size of the screenshot in points (width, height). Defaults to None.
        :param vertical_alignment:      Vertical alignment of the screenshot. Defaults to LayoutElement.VerticalAlignment.TOP.
        :param xdisplay:                The X display string to connect to. Defaults to None.
        """
        from PIL import ImageGrab  # type: ignore[import-untyped, import-not-found]

        super().__init__(
            bytes_path_pil_image_or_url=ImageGrab.grab(
                bbox=bounding_box,
                include_layered_windows=include_layered_windows,
                all_screens=all_screens,
                xdisplay=xdisplay,
            ),
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
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            size=size,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
