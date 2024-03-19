#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the definition of `PageLayout`.
`PageLayout` can be used to add `LayoutElement` objects to a `Page` without
having to specify coordinates.
"""

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class PageLayout:
    """
    This class acts as a layoutmanager for `Document` objects.
    Instead of adding `LayoutElements` to a `Page` by calling `layout` (and needing to know the precise coordinates)
    you can simply use this class and its `add` method.
    Any implementation of `PageLayout` should keep track of where `LayoutElement` objects are placed,
    and what the remaining free space is.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, page: Page):
        self._page = page

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        The specific implementation of `PageLayout` should decide where the `LayoutElement` will be placed.
        :param layout_element:  the LayoutElement to be added
        :return:                self
        """
        return self

    def get_page(self) -> Page:
        """
        This function returns the Page for which this PageLayout is active.
        :return:    the Page
        """
        return self._page
