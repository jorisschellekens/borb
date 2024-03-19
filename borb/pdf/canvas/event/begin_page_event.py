#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered right before the Canvas is being processed.
"""
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.page.page import Page


class BeginPageEvent(Event):
    """
    This implementation of Event is triggered right before the Canvas is being processed.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, page: Page):
        self._page: Page = page

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_page(self) -> Page:
        """
        This function returns the Page that triggered this BeginPageEvent
        :return:    the Page
        """
        return self._page
