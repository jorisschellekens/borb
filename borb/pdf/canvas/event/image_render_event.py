#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered when an Image has been processed using a Do instruction
"""
from decimal import Decimal

from PIL import Image as PILImage  # type: ignore [import]

from borb.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from borb.pdf.canvas.event.event_listener import Event


class ImageRenderEvent(Event):
    """
    This implementation of Event is triggered when an Image has been processed using a Do instruction
    """

    def __init__(self, graphics_state: CanvasGraphicsState, image: PILImage):
        self._image: PILImage = image

        # calculate position
        v = graphics_state.ctm.cross(Decimal(0), Decimal(0), Decimal(1))
        self._x: Decimal = v[0]
        self._y: Decimal = v[1]

        # calculate display size
        v = graphics_state.ctm.cross(Decimal(1), Decimal(1), Decimal(0))
        self._width: Decimal = max(abs(v[0]), Decimal(1))
        self._height: Decimal = max(abs(v[1]), Decimal(1))

    def get_image(self) -> PILImage:
        """
        Get the (source) Image
        This Image may have different dimensions than
        how it is displayed in the PDF
        """
        return self._image

    def get_x(self) -> Decimal:
        """
        Get the x-coordinate at which the Image is drawn
        """
        return self._x

    def get_y(self) -> Decimal:
        """
        Get the y-coordinate at which the Image is drawn
        """
        return self._y

    def get_width(self) -> Decimal:
        """
        Get the width of the (scaled) Image
        """
        return self._width

    def get_height(self) -> Decimal:
        """
        Get the height of the (scaled) Image
        """
        return self._height
