#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a dropdown list for gender selection in a PDF document.

The `GenderDropDownList` class is used to create and manage a dropdown list
form element that allows users to select their gender from predefined options.
This dropdown simplifies data entry by providing a limited set of choices,
enhancing the user experience in PDF forms.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.form.drop_down_list import DropDownList
from borb.pdf.layout_element.layout_element import LayoutElement


class GenderDropDownList(DropDownList):
    """
    Represents a dropdown list for gender selection in a PDF document.

    The `GenderDropDownList` class is used to create and manage a dropdown list
    form element that allows users to select their gender from predefined options.
    This dropdown simplifies data entry by providing a limited set of choices,
    enhancing the user experience in PDF forms.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = X11Color.LIGHT_GRAY,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 1,
        border_width_left: int = 1,
        border_width_right: int = 1,
        border_width_top: int = 1,
        default_value: str = "",
        field_name: typing.Optional[str] = None,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        value: str = "",
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a GenderDropDownList object, representing a dropdown list form element in a PDF.

        :param background_color:        The background color of the dropdown. Defaults to None.
        :param border_color:            The color of the dropdown's border. Defaults to None.
        :param border_dash_pattern:     A list specifying the dash pattern for the border. Defaults to an empty list (solid border).
        :param border_dash_phase:       The phase offset for the border dash pattern. Defaults to 0.
        :param border_width_bottom:     The width of the bottom border of the dropdown. Defaults to 0.
        :param border_width_left:       The width of the left border of the dropdown. Defaults to 0.
        :param border_width_right:      The width of the right border of the dropdown. Defaults to 0.
        :param border_width_top:        The width of the top border of the dropdown. Defaults to 0.
        :param default_value:           The default selected value for the dropdown. Defaults to an empty string.
        :param field_name:              The optional name of the dropdown form field. Defaults to None.
        :param font_color:              The color of the text in the dropdown. Defaults to X11Color.BLACK.
        :param font_size:               The font size of the text in the dropdown. Defaults to 12.
        :param horizontal_alignment:    The horizontal alignment of the dropdown (e.g., left, center, right). Defaults to LEFT.
        :param margin_bottom:           The bottom margin of the dropdown. Defaults to 0.
        :param margin_left:             The left margin of the dropdown. Defaults to 0.
        :param margin_right:            The right margin of the dropdown. Defaults to 0.
        :param margin_top:              The top margin of the dropdown. Defaults to 0.
        :param padding_bottom:          The bottom padding inside the dropdown. Defaults to 0.
        :param padding_left:            The left padding inside the dropdown. Defaults to 0.
        :param padding_right:           The right padding inside the dropdown. Defaults to 0.
        :param padding_top:             The top padding inside the dropdown. Defaults to 0.
        :param value:                   The current value of the dropdown. Defaults to an empty string.
        :param vertical_alignment:      The vertical alignment of the dropdown (e.g., top, middle, bottom). Defaults to TOP.
        """
        assert (
            field_name is None or len(field_name) > 0
        ), "The field_name must be None or a non-empty str."
        super().__init__(
            options=["Female", "Male", "Non-binary", "Prefer Not to Disclose"],
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            default_value=default_value,
            field_name=field_name,
            font_color=font_color,
            font_size=font_size,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            value=value,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
