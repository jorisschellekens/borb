#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event triggered when a shape is stroked on a page.

This event represents the action of stroking a geometric shape or path on a page in a
PDF document. It encapsulates details such as the document and page context, the shape
being stroked, the stroke's line width, and its color. This allows the event to be
processed, analyzed, or modified by components in the PDF processing pipeline.
"""
from borb.pdf.color.color import Color
from borb.pdf.page import Page
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.source.operator.source import ShapeType


class ShapeStrokeEvent(Event):
    """
    Event triggered when a shape is stroked on a page.

    This event represents the action of stroking a geometric shape or path on a page in a
    PDF document. It encapsulates details such as the document and page context, the shape
    being stroked, the stroke's line width, and its color. This allows the event to be
    processed, analyzed, or modified by components in the PDF processing pipeline.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        line_width: float,
        page: Page,
        shape: ShapeType,
        stroke_color: Color,
    ):
        """
        Initialize a new instance of the ShapeStrokeEvent class.

        This constructor creates a shape stroke event, defining the properties of a stroked
        shape on a PDF document. The event includes attributes such as the document and page
        context, the line width, the shape to be stroked, and the stroke color.

        :param line_width:   The width of the line used for stroking the shape. Determines the thickness of the stroke outline.
        :param page:         The specific page of the document where the shape is stroked. Defines the placement context for the event.
        :param shape:        The shape to be stroked. Represents the geometric outline or path being rendered with a stroke.
        :param stroke_color: The color used for stroking the shape. Defines the visual appearance of the stroke.
        """
        super().__init__()
        self.__line_width: float = line_width
        self.__page: Page = page
        self.__shape: ShapeType = shape
        self.__stroke_color: Color = stroke_color

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_height(self) -> float:
        """
        Return the height of the shape's bounding box.

        :return: The height of the bounding box for the shape.
        """
        return (
            max([max(line[0][1], line[1][1]) for line in self.__shape]) - self.get_y()
        )

    def get_page(self) -> Page:
        """
        Return the page where the shape is placed.

        :return: The page in the document where the shape appears.
        """
        return self.__page

    def get_shape(self) -> ShapeType:
        """
        Return the shape being stroked.

        :return: The shape that is being stroked.
        """
        return self.__shape

    def get_stroke_color(self) -> Color:
        """
        Return the color used to stroke the shape.

        :return: The color used for stroking the shape.
        """
        return self.__stroke_color

    def get_width(self) -> float:
        """
        Return the width of the shape's bounding box.

        :return: The width of the bounding box for the shape.
        """
        return (
            max([max(line[0][0], line[1][0]) for line in self.__shape]) - self.get_x()
        )

    def get_x(self) -> float:
        """
        Return the minimum x-coordinate of the shape's bounding box.

        :return: The minimum x-coordinate of the bounding box for the shape.
        """
        return min([min(line[0][0], line[1][0]) for line in self.__shape])

    def get_y(self) -> float:
        """
        Return the minimum y-coordinate of the shape's bounding box.

        :return: The minimum y-coordinate of the bounding box for the shape.
        """
        return min([min(line[0][1], line[1][1]) for line in self.__shape])
