#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a paragraph composed of homogeneous text.

The `HomogeneousParagraph` class is used to create a paragraph where all
text shares the same styling properties, such as font, size, and color.
Unlike `HeterogeneousParagraph`, the text in this paragraph is uniform
and does not vary in style between different parts of the paragraph.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph


class HomogeneousParagraph(HeterogeneousParagraph):
    """
    Represents a paragraph composed of homogeneous text.

    The `HomogeneousParagraph` class is used to create a paragraph where all
    text shares the same styling properties, such as font, size, and color.
    Unlike `HeterogeneousParagraph`, the text in this paragraph is uniform
    and does not vary in style between different parts of the paragraph.
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
        character_spacing: float = 0,
        fixed_leading: typing.Optional[int] = None,
        font: typing.Optional[typing.Union[Font, str]] = None,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        multiplied_leading: typing.Optional[float] = 1.2,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
        word_spacing: float = 0,
    ):
        """
        Initialize a HomogeneousParagraph object with uniform text properties.

        The `HomogeneousParagraph` class represents a paragraph consisting of
        a single text string, allowing for uniform styling across the entire
        paragraph. This class is useful for simple text content that requires
        consistent formatting, such as color and font size.

        :param text:                    The text content of the paragraph, which will be displayed with uniform styling.
        :param font_color:              The color of the font. Defaults to black (X11Color.BLACK).
        :param font_size:               The size of the font in points. Defaults to 12.
        :param font:                    An optional font object. If not provided, a default font will be used.
        :param background_color:        Optional background color for the paragraph. Defaults to None.
        :param fixed_leading:           Optional fixed leading (line spacing) for the paragraph. If provided, it will override multiplied leading.
        :param multiplied_leading:      The factor by which to multiply the font size to calculate line spacing. Default is 1.2.
        :param text_alignment:          The alignment of the text within the paragraph. Defaults to left alignment.
        :param border_color:            Optional color for the border of the paragraph. Defaults to None.
        :param border_dash_pattern:     List defining the dash pattern for the border. Defaults to an empty list.
        :param border_dash_phase:       Phase offset for the dash pattern. Defaults to 0.
        :param border_width_bottom:     Width of the bottom border. Defaults to 0.
        :param border_width_left:       Width of the left border. Defaults to 0.
        :param border_width_right:      Width of the right border. Defaults to 0.
        :param border_width_top:        Width of the top border. Defaults to 0.
        :param horizontal_alignment:    Alignment of the paragraph within its containing element. Defaults to left alignment.
        :param margin_bottom:           Bottom margin around the paragraph. Defaults to 0.
        :param margin_left:             Left margin around the paragraph. Defaults to 0.
        :param margin_right:            Right margin around the paragraph. Defaults to 0.
        :param margin_top:              Top margin around the paragraph. Defaults to 0.
        :param padding_bottom:          Padding inside the bottom of the paragraph. Defaults to 0.
        :param padding_left:            Padding inside the left of the paragraph. Defaults to 0.
        :param padding_right:           Padding inside the right of the paragraph. Defaults to 0.
        :param padding_top:             Padding inside the top of the paragraph. Defaults to 0.
        :param vertical_alignment:      Alignment of the paragraph within its containing element vertically. Defaults to top alignment.
        """
        super().__init__(
            chunks=[
                Chunk(
                    text=text,
                    character_spacing=character_spacing,
                    font=font,
                    font_color=font_color,
                    font_size=font_size,
                    word_spacing=word_spacing,
                )
            ],
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
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self.__font_size: int = font_size
        self.__font_color: Color = font_color
        self.__font: Font = font or Standard14Fonts.get("Helvetica")  # type: ignore[assignment]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_font(self) -> "Font":
        """
        Return the font used for the paragraph.

        This method returns the font object associated with the paragraph,
        which defines the typography and style of the rendered text.

        :return: The font object associated with this Paragraph
        """
        return self.__font

    def get_font_color(self) -> Color:
        """
        Return the font color used for the paragraph.

        This method returns the color object associated with the paragraph,
        which determines the color of the rendered text.

        :return: The color object associated with this Paragraph
        """
        return self.__font_color

    def get_font_size(self) -> int:
        """
        Return the font size used for the paragraph.

        This method returns the font size associated with the paragraph.

        :return: The font size associated with this Paragraph
        """
        return self.__font_size
