#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a two-column layout for a PDF page.

The `TwoColumnLayout` class is a specialized implementation of the
`MultiColumnLayout` that organizes content into exactly two columns.
This layout is designed to facilitate the presentation of information
in a balanced and visually appealing manner, allowing for easy reading
and comprehension. It automatically manages the flow of content, ensuring
that any overflow transitions seamlessly to the next column or page as
needed.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.page_layout.multi_column_layout import MultiColumnLayout


class TwoColumnLayout(MultiColumnLayout):
    """
    Represents a two-column layout for a PDF page.

    The `TwoColumnLayout` class is a specialized implementation of the
    `MultiColumnLayout` that organizes content into exactly two columns.
    This layout is designed to facilitate the presentation of information
    in a balanced and visually appealing manner, allowing for easy reading
    and comprehension. It automatically manages the flow of content, ensuring
    that any overflow transitions seamlessly to the next column or page as
    needed.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        page: Page,
        margin_bottom: typing.Optional[int] = None,
        margin_left: typing.Optional[int] = None,
        margin_right: typing.Optional[int] = None,
        margin_top: typing.Optional[int] = None,
    ):
        """
        Initialize the TwoColumnLayout with the specified page.

        The `TwoColumnLayout` constructor establishes a layout that organizes content
        into two distinct columns on the provided PDF page.
        By invoking the parent class's initializer with the specified page and a fixed number of columns (two),
        this constructor creates the framework for content arrangement.
        This layout is designed to optimize readability and balance by allowing content
        to flow smoothly between the two columns, enhancing the overall presentation.

        :param page:    An instance of the `Page` class that represents the area where the two-column layout will be applied.
                        This page serves as the foundation for the layout, determining its size and any relevant attributes.
        """
        super().__init__(
            number_of_columns=2,
            page=page,
            margin_top=margin_top,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
