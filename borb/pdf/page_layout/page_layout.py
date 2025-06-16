#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A base class for managing the layout of elements on a PDF page.

The `PageLayout` class defines the fundamental structure and behavior for arranging
content on a PDF page. It serves as a foundation for more specific layout types,
such as single-column or multi-column layouts. This class provides core functionality
for positioning and managing various layout elements (e.g., text, images, tables)
within the document.

Subclasses of `PageLayout` can implement different layout strategies, ensuring
flexibility in how content is arranged on the page. This class supports method chaining
for appending elements and adjusting layouts dynamically.
"""
from borb.pdf.layout_element.layout_element import LayoutElement


class PageLayout:
    """
    A base class for managing the layout of elements on a PDF page.

    The `PageLayout` class defines the fundamental structure and behavior for arranging
    content on a PDF page. It serves as a foundation for more specific layout types,
    such as single-column or multi-column layouts. This class provides core functionality
    for positioning and managing various layout elements (e.g., text, images, tables)
    within the document.

    Subclasses of `PageLayout` can implement different layout strategies, ensuring
    flexibility in how content is arranged on the page. This class supports method chaining
    for appending elements and adjusting layouts dynamically.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def append_layout_element(self, layout_element: LayoutElement) -> "PageLayout":
        """
        Append a layout element to the page layout.

        This method adds the specified layout element, such as text, images, or other
        visual components, to the current page layout. The element is positioned according
        to the layout's structure, which may vary depending on the specific layout
        implementation (e.g., single-column, multi-column). It ensures that content
        is organized and presented appropriately.

        :param layout_element:   the LayoutElement to be added
        :return:    Self, this allows for method-chaining
        """
        return self
