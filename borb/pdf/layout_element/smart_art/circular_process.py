#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a circular process layout that visually organizes a series of steps or items in a looped, radial arrangement to emphasize cyclic or continuous progression.

This class is designed to display items evenly distributed around a circle,
visually reinforcing the concept of repetition, feedback loops, or perpetual flow.
Each item represents a step or stage in the process, with arrows or connectors
indicating directionality—typically clockwise. This layout is ideal for systems
that repeat, evolve in stages, or emphasize closed-loop structures such as life
cycles, iterative processes, or circular economies.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.meta.circular_layout_element_group import (
    CircularLayoutElementGroup,
)
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.layout_element.text.paragraph import Paragraph


class CircularProcess:
    """
    Represents a circular process layout that visually organizes a series of steps or items in a looped, radial arrangement to emphasize cyclic or continuous progression.

    This class is designed to display items evenly distributed around a circle,
    visually reinforcing the concept of repetition, feedback loops, or perpetual flow.
    Each item represents a step or stage in the process, with arrows or connectors
    indicating directionality—typically clockwise. This layout is ideal for systems
    that repeat, evolve in stages, or emphasize closed-loop structures such as life
    cycles, iterative processes, or circular economies.
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

    @staticmethod
    def build(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a circular process layout with items arranged radially around a center.

        This static method creates a visual layout of a process, placing each
        item (level 1) evenly spaced around a circle to represent cyclical flow
        or repeating sequences. Arrows connect items in a clockwise direction,
        emphasizing the ongoing, looped nature of the process.

        :param level_1_items:       A list of strings representing the primary items or steps in the process.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for item labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed circular process layout, ready for rendering in a graphical interface.
        """
        # create a (much) lighter background color
        lighter_background_color = background_color
        for _ in range(0, 5):
            lighter_background_color = lighter_background_color.lighter()

        # build the LayoutElements
        elements: typing.List[LayoutElement] = []
        sizes: typing.List[typing.Tuple[int, int]] = []
        for i in range(0, len(level_1_items)):

            # add paragraph
            elements += [
                Paragraph(
                    level_1_items[i],
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                    background_color=background_color,
                    font_color=level_1_font_color,
                    padding_top=level_1_font_size // 3,
                    padding_right=level_1_font_size // 3,
                    padding_bottom=level_1_font_size // 3,
                    padding_left=level_1_font_size // 3,
                    font_size=level_1_font_size,
                )
            ]

            # fmt: off
            sizes += [CircularLayoutElementGroup._CircularLayoutElementGroup__golden_ratio_landscape_box(elements[-1])] # type: ignore[attr-defined]
            # fmt: on

            # add arrow
            elements += [
                LineArt.arrow_down(
                    fill_color=lighter_background_color,
                    line_width=1,
                    stroke_color=lighter_background_color,
                )
            ]

            # force alignment
            # fmt: off
            elements[-1]._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE    # type: ignore[attr-defined]
            elements[-1]._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE        # type: ignore[attr-defined]
            # fmt: on

            sizes += [(-1, -1)]

        # calculate average width/height
        average_width = sum([s[0] for s in sizes if s != (-1, -1)]) // len(sizes)
        average_height = sum([s[1] for s in sizes if s != (-1, -1)]) // len(sizes)
        average_width = max(average_width, 16)
        average_height = max(average_height, 16)

        # set size for arrows
        sizes = [
            (x[0], x[1]) if x != (-1, -1) else (average_width, average_height)
            for x in sizes
        ]

        # scale arrows
        angle = 360 / len(level_1_items)
        for i, l in enumerate(elements):
            if isinstance(l, Shape):
                elements[i] = elements[i].rotate(-angle * (i // 2) - angle // 2)  # type: ignore[attr-defined]

                # scale
                # fmt: off
                elements[i] = elements[i].scale_to_fit(size=(average_width, average_height))    # type: ignore[attr-defined]
                # fmt: on

                # force alignment
                # fmt: off
                elements[-1]._LayoutElement__horizontal_alignment = LayoutElement.HorizontalAlignment.MIDDLE    # type: ignore[attr-defined]
                elements[-1]._LayoutElement__vertical_alignment = LayoutElement.VerticalAlignment.MIDDLE        # type: ignore[attr-defined]
                # fmt: on

        # build CircularLayoutElementGroup
        return CircularLayoutElementGroup(layout_elements=elements, sizes=sizes)
