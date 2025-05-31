#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Event triggered when a page finishes rendering.

This event encapsulates the details of a page being fully rendered in the PDF content stream.
It marks the end of the rendering process for a specific page, providing information about the
page that was rendered, such as the page number and any other relevant details. This event is
triggered once all content for a page has been processed, allowing other components in the PDF
generation pipeline to handle post-processing or cleanup tasks associated with the page.
"""
from borb.pdf.page import Page
from borb.pdf.toolkit.event import Event


class EndPageEvent(Event):
    """
    Event triggered when a page finishes rendering.

    This event encapsulates the details of a page being fully rendered in the PDF content stream.
    It marks the end of the rendering process for a specific page, providing information about the
    page that was rendered, such as the page number and any other relevant details. This event is
    triggered once all content for a page has been processed, allowing other components in the PDF
    generation pipeline to handle post-processing or cleanup tasks associated with the page.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, page: Page):
        """
        Initialize an EndPageEvent instance.

        :param page: The page that has finished rendering.
        """
        super().__init__()
        self.__page: Page = page

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_page(self) -> Page:
        """
        Return the page that has finished rendering.

        :return: The page that was rendered.
        """
        return self.__page
