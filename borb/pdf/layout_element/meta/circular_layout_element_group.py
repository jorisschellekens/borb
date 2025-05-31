#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A group of layout elements arranged in a circular pattern with specified sizes.

This class represents a collection of `LayoutElement` objects, each positioned along
a circular path with predefined sizes. It extends `LayoutElement` and supports rendering
onto a `Page` while respecting layout properties such as alignment, margins, padding, and borders.
"""
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.meta.layout_element_group import LayoutElementGroup
from borb.pdf.layout_element.text.paragraph import Paragraph


class CircularLayoutElementGroup(LayoutElementGroup):
    """
    A group of layout elements arranged in a circular pattern with specified sizes.

    This class represents a collection of `LayoutElement` objects, each positioned along
    a circular path with predefined sizes. It extends `LayoutElement` and supports rendering
    onto a `Page` while respecting layout properties such as alignment, margins, padding, and borders.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        layout_elements: typing.List[LayoutElement],
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
        sizes: typing.Optional[typing.List[typing.Tuple[int, int]]] = None,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new CircularLayoutElementGroup object for rendering a group of LayoutElements in a PDF.

        This constructor allows customization of various layout and style properties
        for the group, such as margins, padding, borders, and alignment. These properties
        define the appearance and positioning of the group within the PDF page.

        :param layout_elements:         The LayoutElement objects in this group
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
        :param sizes:                   The (absolute) sizes of the LayoutElements in this group
        :param vertical_alignment:      Vertical alignment of the list (default is TOP).
        """
        # IF sizes is None
        # THEN calculate sizes (assuming all layout_elements are Paragraphs)
        assert (sizes is not None) or all(
            [isinstance(x, Paragraph) for x in layout_elements]
        )
        sizes = sizes or [
            CircularLayoutElementGroup.__golden_ratio_landscape_box(x)  # type: ignore[arg-type]
            for x in layout_elements
        ]

        # calculate largest circle radius
        max_circle_radius: int = max([(w**2 + h**2) ** 0.5 // 2 for w, h in sizes])

        # calculate coordinates
        K: int = len(layout_elements)
        R: int = math.ceil((max_circle_radius * 2) / (2 * math.sin(math.pi / K)))
        positions: typing.List[typing.Tuple[int, int]] = []
        for i in range(0, K):
            # calculate the midpoint
            mid_x: int = int(math.cos(i * 2 * math.pi / K) * R)
            mid_y: int = int(math.sin(i * 2 * math.pi / K) * R)

            # calculate lower left corner
            x: int = mid_x - sizes[i][0] // 2
            y: int = mid_y - sizes[i][1] // 2

            # append
            positions.append((x, y))

        # call to super
        super().__init__(
            layout_elements=layout_elements,
            sizes=sizes,
            positions=positions,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            background_color=background_color,
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

    #
    # PRIVATE
    #

    @staticmethod
    def __golden_ratio_landscape_box(p: Paragraph) -> typing.Tuple[int, int]:
        golden_ratio: float = (1 + 5**0.5) / 2
        best_width: typing.Optional[int] = None
        best_height: typing.Optional[int] = None
        best_delta: typing.Optional[float] = None
        for w in range(595, 1, -5):
            try:
                h: int = p.get_size(available_space=(w, 842))[1]
                if h > 842:
                    continue
                ratio: float = w / h
                delta: float = abs(golden_ratio - ratio)
                if best_delta is None or delta < best_delta:
                    best_width = w
                    best_height = h
                    best_delta = delta
            except:
                continue
        assert best_width is not None
        assert best_height is not None
        return best_width, best_height

    #
    # PUBLIC
    #
