#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event triggered when an image is placed on a page.

This event encapsulates the details of an image being placed on a page, including its
dimensions, position, the PDF image object, and other related information. It allows
the event to be processed or handled by other components in the PDF generation pipeline.
"""
from borb.pdf.page import Page
from borb.pdf.primitives import name, PDFType
from borb.pdf.toolkit.event import Event


class ImageEvent(Event):
    """
    Event triggered when an image is placed on a page.

    This event encapsulates the details of an image being placed on a page, including its
    dimensions, position, the PDF image object, and other related information. It allows
    the event to be processed or handled by other components in the PDF generation pipeline.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        height: float,
        image: PDFType,
        page: Page,
        width: float,
        x: float,
        xobject_resource: name,
        y: float,
    ):
        """
        Initialize an ImageEvent instance.

        :param height:              The height of the image in user space.
        :param image:               The image (of type PDFType) to be placed on the page.
        :param page:                The page on which the image will be placed.
        :param width:               The width of the image in user space.
        :param x:                   The x-coordinate where the image will be placed.
        :param xobject_resource:    The name of the XObject resource representing the image.
        :param y:                   The y-coordinate where the image will be placed.
        """
        self.__height: float = height
        self.__image: PDFType = image
        self.__page: Page = page
        self.__width: float = width
        self.__x: float = x
        self.__xobject_resource: name = xobject_resource
        self.__y: float = y

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_height(self) -> float:
        """
        Return the height of the image.

        :return: The height of the image.
        """
        return self.__height

    def get_image(self) -> PDFType:
        """
        Return the image associated with this event.

        :return: The image content or object associated with the event.
        """
        return self.__image

    def get_page(self) -> Page:
        """
        Return the page where the image is placed.

        :return: The page in the document where the image appears.
        """
        return self.__page

    def get_width(self) -> float:
        """
        Return the width of the image.

        :return: The width of the image.
        """
        return self.__width

    def get_x(self) -> float:
        """
        Return the x-coordinate (horizontal position) of the image.

        :return: The x-coordinate of the image.
        """
        return self.__x

    def get_xobject_resource(self) -> name:
        """
        Return the XObject resource name associated with the image.

        :return: The XObject resource name associated with the image.
        """
        return self.__xobject_resource

    def get_y(self) -> float:
        """
        Return the y-coordinate (vertical position) of the image.

        :return: The y-coordinate of the image.
        """
        return self.__y
