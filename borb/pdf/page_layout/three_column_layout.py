#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a three-column layout for a PDF page.

The `TwoColumnLayout` class is a specialized implementation of the
`MultiColumnLayout` that organizes content into exactly three columns.
This layout is designed to facilitate the presentation of information
in a balanced and visually appealing manner, allowing for easy reading
and comprehension. It automatically manages the flow of content, ensuring
that any overflow transitions seamlessly to the next column or page as
needed.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.page_layout.multi_column_layout import MultiColumnLayout


class ThreeColumnLayout(MultiColumnLayout):
    """
    Represents a three-column layout for a PDF page.

    The `ThreeColumnLayout` class is a specialized implementation of the
    `MultiColumnLayout` that organizes content into exactly three columns.
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
        Initialize the ThreeColumnLayout with the specified page.

        The `ThreeColumnLayout` constructor sets up a layout that organizes content
        into three distinct columns on the provided PDF page.
        By calling the parent class's initializer with the specified page and a fixed number of columns (three),
        this constructor establishes the necessary framework for content arrangement.
        The layout is designed to optimize space utilization and enhance readability,
        automatically managing content flow between columns and pages.

        :param page:    An instance of the `Page` class that defines the area where the three-column layout will be applied.
                        This page serves as the canvas for the layout, determining its dimensions and any other relevant properties.
        """
        super().__init__(
            number_of_columns=3,
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
