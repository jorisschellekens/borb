#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a button form element that executes JavaScript code in a PDF document.

The `JavaScriptButton` class is used to create interactive buttons that trigger
JavaScript actions when clicked. These buttons enhance the functionality of PDF
forms by enabling dynamic behaviors, such as form validation, calculations, or
displaying alerts. This class allows for a more interactive user experience within
PDF documents.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.form.button import Button
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import stream, name


class JavascriptButton(Button):
    """
    Represents a button form element that executes JavaScript code in a PDF document.

    The `JavaScriptButton` class is used to create interactive buttons that trigger
    JavaScript actions when clicked. These buttons enhance the functionality of PDF
    forms by enabling dynamic behaviors, such as form validation, calculations, or
    displaying alerts. This class allows for a more interactive user experience within
    PDF documents.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        javascript: str,
        text: str,
        background_color: typing.Optional[Color] = X11Color.LIGHT_GRAY,
        border_color: typing.Optional[Color] = X11Color.GRAY,
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
        Initialize a JavascriptButton component, representing a button form field that can be inserted into a PDF document.

        :param javascript:              The javascript code executed when clicking this Button
        :param text:                    The text shown on the (javascript) Button
        :param background_color:        Optional; The background color of the text box. If None, the background is transparent.
        :param border_color:            Optional; The color of the border around the text box. If None, no border will be drawn.
        :param border_dash_pattern:     A list of integers defining the dash pattern for the border. For example, [5, 3] creates a dashed border.
        :param border_dash_phase:       The phase at which the dash pattern should start. Defaults to 0.
        :param border_width_bottom:     The width of the bottom border in pixels. Defaults to 0 (no bottom border).
        :param border_width_left:       The width of the left border in pixels. Defaults to 0 (no left border).
        :param border_width_right:      The width of the right border in pixels. Defaults to 0 (no right border).
        :param border_width_top:        The width of the top border in pixels. Defaults to 0 (no top border).
        :param default_value:           The default text that appears in the text box when no user input is provided.
        :param field_name:              Optional; The name of the text field. This can be used to identify the field within the PDF.
        :param font_color:              The color of the text within the text box. Defaults to black.
        :param font_size:               The size of the font used for the text within the text box. Defaults to 12.
        :param horizontal_alignment:    Defines the horizontal alignment of the text. Can be LEFT, CENTER, or RIGHT. Defaults to LEFT.
        :param margin_bottom:           The bottom margin of the text box in pixels. Defaults to 0.
        :param margin_left:             The left margin of the text box in pixels. Defaults to 0.
        :param margin_right:            The right margin of the text box in pixels. Defaults to 0.
        :param margin_top:              The top margin of the text box in pixels. Defaults to 0.
        :param padding_bottom:          The bottom padding inside the text box in pixels. Defaults to 0.
        :param padding_left:            The left padding inside the text box in pixels. Defaults to 0.
        :param padding_right:           The right padding inside the text box in pixels. Defaults to 0.
        :param padding_top:             The top padding inside the text box in pixels. Defaults to 0.
        :param value:                   The current value (text content) of the text box. Defaults to an empty string.
        :param vertical_alignment:      Defines the vertical alignment of the text. Can be TOP, MIDDLE, or BOTTOM. Defaults to TOP.
        """
        super().__init__(
            text=text,
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
        self.__javascript: str = javascript

    #
    # PRIVATE
    #

    def __init_widget_dictionary(
        self,
        available_space: typing.Tuple[int, int, int, int],
        document: Document,
        page: Page,
    ):
        # call to super
        super().__init_widget_dictionary(
            available_space=available_space, document=document, page=page
        )

        # build JavaScript stream object
        # fmt: off
        import zlib
        javascript_deflated_bytes: bytes = zlib.compress(self.__javascript.encode('latin1'), 9)
        javascript_stream = stream({
            name("Type"): name("JavaScript"),
            name("Bytes"): javascript_deflated_bytes,
            name('Length'): len(javascript_deflated_bytes),
            name('Filter'): name('FlateDecode'),
        })
        # fmt: on

        # modify action dictionary of PushButton (super)
        # fmt: off
        if self.__widget_dictionary is not None:
            self.__widget_dictionary[name("AA")][name("D")][name("S")] = name("JavaScript")     # type: ignore[index, call-overload]
            self.__widget_dictionary[name("AA")][name("D")][name("JS")] = javascript_stream     # type: ignore[index, call-overload]
        # fmt: on

    #
    # PUBLIC
    #
