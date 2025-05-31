#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event triggered when text is placed on a page.

This event represents the action of rendering a text string on a PDF page. It captures
essential details about the text, including its position, font, font size, font color,
and the content itself. This allows the event to be processed, analyzed, or modified by
components in the PDF processing pipeline.
"""
from borb.pdf.color.color import Color
from borb.pdf.font.font import Font
from borb.pdf.page import Page
from borb.pdf.toolkit.event import Event


class TextEvent(Event):
    """
    Event triggered when text is placed on a page.

    This event represents the action of rendering a text string on a PDF page. It captures
    essential details about the text, including its position, font, font size, font color,
    and the content itself. This allows the event to be processed, analyzed, or modified by
    components in the PDF processing pipeline.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        s: str,
        x: float,
        y: float,
        width: float,
        height: float,
        font: Font,
        font_color: Color,
        font_size: float,
        page: Page,
    ):
        """
        Initialize a new instance of the TextEvent class.

        This constructor creates a text event with the specified properties, defining the
        content and appearance of a text string in a PDF document. The event includes
        attributes such as the text content, position, dimensions, font, color, and associated
        document and page.

        :param s:           The text string to be rendered. Represents the actual content of the text event.
        :param x:           The x-coordinate in user space where the text will be placed. Specifies the horizontal starting point of the text.
        :param y:           The y-coordinate in user space where the text will be placed. Specifies the vertical starting point of the text.
        :param width:       The width of the text's bounding box in user space. Used for layout and alignment calculations.
        :param height:      The height of the text's bounding box in user space. Useful for determining positioning relative to other content.
        :param font:        The font used for rendering the text. Determines the style, weight, and typeface of the text.
        :param font_color:  The color of the text. Defines the visual appearance of the text color.
        :param font_size:   The size of the font used for rendering the text. Controls the scaling of the text content.
        :param page:        The specific page of the document where the text is rendered. Defines the placement context for the event.
        """
        super().__init__()
        self.__page: Page = page
        self.__s: str = s
        self.__x: float = x
        self.__y: float = y
        self.__width: float = width
        self.__height: float = height
        self.__font: Font = font
        self.__font_color: Color = font_color
        self.__font_size: float = font_size

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_font(self) -> Font:
        """
        Retrieve the font used for the text event.

        :return: The `Font` object representing the typeface used in the text event.
        """
        return self.__font

    def get_font_color(self) -> Color:
        """
        Retrieve the font color used for the text event.

        :return: A `Color` object representing the font color.
        """
        return self.__font_color

    def get_font_size(self) -> float:
        """
        Retrieve the font size used for the text event.

        :return: A float representing the size of the font in points.
        """
        return self.__font_size

    def get_height(self) -> float:
        """
        Return the height of the text.

        :return: The height of the text.
        """
        return self.__height

    def get_page(self) -> Page:
        """
        Return the page where the text is placed.

        :return: The page in the document where the text appears.
        """
        return self.__page

    def get_text(self) -> str:
        """
        Retrieve the text content of the text event.

        :return: A string containing the text for the event.
        """
        return self.__s

    def get_width(self) -> float:
        """
        Return the width of the text.

        :return: The width of the text.
        """
        return self.__width

    def get_x(self) -> float:
        """
        Retrieve the x-coordinate of the text event.

        :return: A float representing the x-coordinate of the text's position.
        """
        return self.__x

    def get_y(self) -> float:
        """
        Retrieve the y-coordinate of the text event.

        :return: A float representing the y-coordinate of the text's position.
        """
        return self.__y
