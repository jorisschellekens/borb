#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a single-column layout for a PDF page.

The `TwoColumnLayout` class is a specialized implementation of the
`MultiColumnLayout` that organizes content into exactly one column.
This layout is designed to facilitate the presentation of information
in a balanced and visually appealing manner, allowing for easy reading
and comprehension. It automatically manages the flow of content, ensuring
that any overflow transitions seamlessly to the next column or page as
needed.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.page_layout.multi_column_layout import MultiColumnLayout


class SingleColumnLayout(MultiColumnLayout):
    """
    Represents a single-column layout for a PDF page.

    The `TwoColumnLayout` class is a specialized implementation of the
    `MultiColumnLayout` that organizes content into exactly one column.
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
        Initialize the SingleColumnLayout with the specified page.

        The `SingleColumnLayout` constructor sets up a layout that organizes content
        into a single column on the provided PDF page.
        This layout is ideal for documents where simplicity and clarity are paramount,
        allowing content to flow vertically from the top to the bottom of the page without distraction.
        The constructor calculates the page dimensions and sets appropriate margins for the left, right, top,
        and bottom sides to ensure that content is well-spaced and visually appealing.

        :param p:   An instance of the `Page` class that represents the page where the single-column layout will be applied.
                    This instance provides the dimensions and properties necessary for the layout configuration.
        """
        super().__init__(
            number_of_columns=1,
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
