#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a list of `LayoutElement` objects used in the creation of PDFs.

The `List` class maintains an internal collection of `LayoutElement` instances,
allowing for the addition and manipulation of layout elements such as text, images,
and other content types. This class provides methods to append new elements and
supports method chaining for convenience in building complex document structures.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement


class List(LayoutElement):
    """
    Represents a list of `LayoutElement` objects used in the creation of PDFs.

    The `List` class maintains an internal collection of `LayoutElement` instances,
    allowing for the addition and manipulation of layout elements such as text, images,
    and other content types. This class provides methods to append new elements and
    supports method chaining for convenience in building complex document structures.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new List object for rendering list elements in a PDF.

        This constructor allows customization of various layout and style properties
        for the list, such as margins, padding, borders, and alignment. These properties
        define the appearance and positioning of the list within the PDF page.

        :param background_color:        Optional background color for the list container.
        :param border_color:            Optional border color for the list container.
        :param border_dash_pattern:     Dash pattern used for the list border lines.
        :param border_dash_phase:       Phase offset for the dash pattern in the list borders.
        :param border_width_bottom:     Width of the bottom border of the list.
        :param border_width_left:       Width of the left border of the list.
        :param border_width_right:      Width of the right border of the list.
        :param border_width_top:        Width of the top border of the list.
        :param horizontal_alignment:    Horizontal alignment of the list (default is LEFT).
        :param margin_bottom:           Space between the list and the element below it.
        :param margin_left:             Space between the list and the left page margin.
        :param margin_right:            Space between the list and the right page margin.
        :param margin_top:              Space between the list and the element above it.
        :param padding_bottom:          Padding inside the list container at the bottom.
        :param padding_left:            Padding inside the list container on the left side.
        :param padding_right:           Padding inside the list container on the right side.
        :param padding_top:             Padding inside the list container at the top.
        :param vertical_alignment:      Vertical alignment of the list (default is TOP).
        """
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self.__list_items: typing.List[LayoutElement] = []

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def append_layout_element(self, layout_element: LayoutElement) -> "List":
        """
        Add a layout element to the list and update the index.

        This method adds a layout element (such as a text block, image, or another element)
        to the ordered list and updates the list's index by appending a new index item
        (e.g., a numbered label). The index for the newly added item is automatically
        incremented and formatted as a numbered chunk.

        :param layout_element:   The LayoutElement to be added.
        :return:    Self, to allow for method chaining.
        """
        self.__list_items.append(layout_element)
        return self
