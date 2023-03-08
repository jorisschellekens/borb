#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    In computer science and visualization, a canvas is a container that holds various drawing elements
    (lines, shapes, text, frames containing other elements, etc.).
    It takes its name from the canvas used in visual arts.
"""

from borb.io.read.types import Dictionary
from borb.pdf.canvas.canvas_graphics_state import CanvasGraphicsState


class Canvas(Dictionary):
    """
    In computer science and visualization, a canvas is a container that holds various drawing elements
    (lines, shapes, text, frames containing other elements, etc.).
    It takes its name from the canvas used in visual arts.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(Canvas, self).__init__()
        # compatibility mode
        self.in_compatibility_section = False
        # set initial graphics state
        self.graphics_state = CanvasGraphicsState()
        # canvas tag hierarchy is (oddly enough) not considered to be part of the graphics state
        self.marked_content_stack = []
        # set graphics state stack
        self.graphics_state_stack = []

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
