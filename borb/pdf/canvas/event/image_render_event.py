#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered when an Image has been processed using a Do instruction
"""
from decimal import Decimal

from PIL import Image as PILImageModule

from borb.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from borb.pdf.canvas.event.event_listener import Event


class ImageRenderEvent(Event):
    """
    This implementation of Event is triggered when an Image has been processed using a Do instruction
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self, graphics_state: CanvasGraphicsState, image: PILImageModule.Image
    ):
        self._image: PILImageModule.Image = image

        # calculate position
        v = graphics_state.ctm.cross(Decimal(0), Decimal(0), Decimal(1))
        self._x: Decimal = v[0]
        self._y: Decimal = v[1]

        # calculate display size
        v = graphics_state.ctm.cross(Decimal(1), Decimal(1), Decimal(0))
        self._width: Decimal = max(abs(v[0]), Decimal(1))
        self._height: Decimal = max(abs(v[1]), Decimal(1))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_height(self) -> Decimal:
        """
        Get the height at which the Image is drawn
        :return:    the height
        """
        return self._height

    def get_image(self) -> PILImageModule.Image:
        """
        Get the PIL.Image.Image as it is stored in the PDF.
        This Image may have different dimensions from how the Image is drawn in the PDF
        :return:    the Image
        """
        return self._image

    def get_width(self) -> Decimal:
        """
        Get the width at which the Image is drawn
        :return:    the width
        """
        return self._width

    def get_x(self) -> Decimal:
        """
        Get the x-coordinate at which the Image is drawn
        :return:    the x-coordinate
        """
        return self._x

    def get_y(self) -> Decimal:
        """
        Get the y-coordinate at which the Image is drawn
        :return:    the y-coordinate
        """
        return self._y
