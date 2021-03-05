#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered when an Image has been processed using a Do instruction
"""
from decimal import Decimal

from PIL import Image  # type: ignore [import]

from ptext.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from ptext.pdf.canvas.event.event_listener import Event


class ImageRenderEvent(Event):
    """
    This implementation of Event is triggered when an Image has been processed using a Do instruction
    """

    def __init__(self, graphics_state: CanvasGraphicsState, image: Image):
        self.image = image

        # calculate position
        v = graphics_state.ctm.cross(0, 0, 1)
        self.x = v[0]
        self.y = v[1]

        # calculate display size
        v = graphics_state.ctm.cross(1, 1, 0)
        self.width = max(abs(v[0]), Decimal(1))
        self.height = max(abs(v[1]), Decimal(1))

    def get_image(self) -> Image:
        """
        Get the (source) Image
        This Image may have different dimensions than
        how it is displayed in the PDF
        """
        return self.image

    def get_x(self) -> Decimal:
        """
        Get the x-coordinate at which the Image is drawn
        """
        return self.x

    def get_y(self) -> Decimal:
        """
        Get the y-coordinate at which the Image is drawn
        """
        return self.y

    def get_width(self) -> Decimal:
        """
        Get the width of the (scaled) Image
        """
        return self.width

    def get_height(self) -> Decimal:
        """
        Get the height of the (scaled) Image
        """
        return self.height
