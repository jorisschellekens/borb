#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event triggered when a shape is filled on a page.

This event represents the action of filling a shape on a PDF page. It holds all the
necessary data to describe the shape, its fill color, and whether the even-odd rule
is used for determining which areas to fill. The event encapsulates information that
can be used by other components to process or render the filled shape on the page.
"""
from borb.pdf.color.color import Color
from borb.pdf.page import Page
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.source.operator.source import ShapeType


class ShapeFillEvent(Event):
    """
    Event triggered when a shape is filled on a page.

    This event represents the action of filling a shape on a PDF page. It holds all the
    necessary data to describe the shape, its fill color, and whether the even-odd rule
    is used for determining which areas to fill. The event encapsulates information that
    can be used by other components to process or render the filled shape on the page.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        fill_color: Color,
        page: Page,
        shape: ShapeType,
        use_even_odd_rule: bool,
    ):
        """
        Initialize a ShapeFillEvent instance.

        :param fill_color: The color used to fill the shape.
        :param page: The page on which the shape is being filled.
        :param shape: The shape being filled.
        :param use_even_odd_rule: Flag indicating whether the even-odd rule is used
                                   for filling the shape.
        """
        super().__init__()
        self.__fill_color: Color = fill_color
        self.__page: Page = page
        self.__shape: ShapeType = shape
        self.__use_even_odd_rule: bool = use_even_odd_rule

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_fill_color(self) -> Color:
        """
        Return the color used to fill the shape.

        :return: The color used for filling the shape.
        """
        return self.__fill_color

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
        Return the shape being filled.

        :return: The shape that is being filled.
        """
        return self.__shape

    def get_use_even_odd_rule(self) -> bool:
        """
        Return whether the even-odd rule is used for determining the fill area.

        :return: True if the even-odd rule is used, False otherwise.
        """
        return self.__use_even_odd_rule

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
