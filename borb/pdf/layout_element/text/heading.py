#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a heading element in a PDF document.

The `Heading` class is designed to create and manage heading elements
within a PDF document. It not only defines the visual properties of the
heading (such as size and style) but also ensures that the heading entries
are correctly set in the PDF outline data structure. This functionality
is crucial for enabling PDF reading software to display the headings
in a structured and navigable manner, improving document accessibility.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page


class Heading(Paragraph):
    """
    Represents a heading element in a PDF document.

    The `Heading` class is designed to create and manage heading elements
    within a PDF document. It not only defines the visual properties of the
    heading (such as size and style) but also ensures that the heading entries
    are correctly set in the PDF outline data structure. This functionality
    is crucial for enabling PDF reading software to display the headings
    in a structured and navigable manner, improving document accessibility.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        text: str,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        fixed_leading: typing.Optional[int] = None,
        font: typing.Optional[Font] = None,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        multiplied_leading: typing.Optional[float] = 1.2,
        outline_level: int = 1,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a Heading object for a PDF document.

        The `Heading` class represents a heading element in the PDF document, combining the functionality of a
        `Paragraph` with special behavior for updating the PDF's internal structure to support a navigable
        document outline (Table of Contents) in PDF viewers. Headings are used to structure the document and
        enable hierarchical navigation.

        This constructor allows for the configuration of the heading's text, visual styling, alignment, and its
        contribution to the document outline. The `level` parameter defines the hierarchy of the heading, where
        smaller numbers (e.g., 1) represent higher levels in the hierarchy (like H1, H2, etc.).

        :param text:                   The text content of the heading.
        :param outline_level:          The level of the heading in the document hierarchy (default is 1).
        :param font:                   The font to use for the heading text (optional).
        :param font_size:              The size of the font for the heading (default is 16).
        :param font_color:             The color of the heading text (default is black).
        :param background_color:       The background color behind the heading (optional).
        :param border_color:           The color of the heading's border (optional).
        :param border_dash_pattern:    The dash pattern for the heading's border (default is solid).
        :param border_dash_phase:      The phase of the dash pattern for the border (default is 0).
        :param border_width_bottom:    The width of the bottom border (default is 0).
        :param border_width_left:      The width of the left border (default is 0).
        :param border_width_right:     The width of the right border (default is 0).
        :param border_width_top:       The width of the top border (default is 0).
        :param horizontal_alignment:   The horizontal alignment of the heading text (default is left-aligned).
        :param margin_bottom:          The margin below the heading (default is 10).
        :param margin_left:            The margin to the left of the heading (default is 0).
        :param margin_right:           The margin to the right of the heading (default is 0).
        :param margin_top:             The margin above the heading (default is 10).
        :param padding_bottom:         The padding below the heading text (default is 0).
        :param padding_left:           The padding to the left of the heading text (default is 0).
        :param padding_right:          The padding to the right of the heading text (default is 0).
        :param padding_top:            The padding above the heading text (default is 0).
        :param vertical_alignment:     The vertical alignment of the heading text (default is top-aligned).
        """
        super().__init__(
            text=text,
            font_color=font_color,
            font_size=font_size,
            font=font,
            background_color=background_color,
            fixed_leading=fixed_leading,
            multiplied_leading=multiplied_leading,
            text_alignment=text_alignment,
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
            padding_bottom=padding_bottom
            or Heading.__get_padding_for_outline_level(
                outline_level=outline_level, font_size=font_size
            ),
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top
            or Heading.__get_padding_for_outline_level(
                outline_level=outline_level, font_size=font_size
            ),
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __get_padding_for_outline_level(
        font_size: int = 12,
        outline_level: int = 0,
    ) -> int:
        return int(
            {
                1: 0.335,
                2: 0.553,
                3: 0.855,
                4: 1.333,
                5: 2.012,
                6: 3.477,
            }.get(outline_level + 1, 1.2)
            * font_size
        )

    #
    # PUBLIC
    #

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        super().paint(available_space=available_space, page=page)

        # TODO
