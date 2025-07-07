#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a single-line text entry form element in a PDF document.

The `TextBox` class is used to create and manage text input fields that allow
users to enter a single line of text within PDF forms. Text boxes are ideal for
capturing brief inputs such as names, email addresses, or other concise data.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.form.form_field import FormField
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name, stream


class TextBox(FormField):
    """
    Represents a single-line text entry form element in a PDF document.

    The `TextBox` class is used to create and manage text input fields that allow
    users to enter a single line of text within PDF forms. Text boxes are ideal for
    capturing brief inputs such as names, email addresses, or other concise data.
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
        max_size: typing.Optional[int] = None,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        value: str = "",
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a TextBox component, representing a text box form field that can be inserted into a PDF document.

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
        assert (
            field_name is None or len(field_name) > 0
        ), "The field_name must be None or a non-empty str."
        assert font_size > 0, "The font_size must be a non-negative value."
        assert (max_size is None) or (
            max_size > 0
        ), "The max_size must be a non-negative value."
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
        self.__value: str = value
        self.__default_value: str = default_value
        self.__font_size: int = font_size
        self.__field_name: typing.Optional[str] = field_name
        self.__font_color: Color = font_color
        self.__max_size: typing.Optional[int] = max_size
        self.__widget_dictionary: typing.Optional[typing.Dict[str, PDFType]] = None

    #
    # PRIVATE
    #

    def __init_widget_dictionary(
        self,
        available_space: typing.Tuple[int, int, int, int],
        document: Document,
        page: Page,
    ):
        font_color_rgb: RGBColor = self.__font_color.to_rgb_color()
        r: float = round(font_color_rgb.get_red() / 255, 8)
        g: float = round(font_color_rgb.get_green() / 255, 8)
        b: float = round(font_color_rgb.get_blue() / 255, 8)

        # fmt: off
        font_name: name = self._FormField__get_font_resource_name(font=Standard14Fonts.get("Helvetica"), page=page) # type: ignore[arg-type, attr-defined]
        # fmt: on

        self.__widget_dictionary = {
            name("AP"): {
                name("N"): stream(
                    {
                        name("BBox"): [0, 0, available_space[2], available_space[3]],
                        name(
                            "Bytes"
                        ): b"x\x9c\xd3\x0f\xa9Pp\xf2uVp\xf5u\x06\x00\x11\xa7\x02\xe3",
                        name("Resources"): document["Trailer"]["Root"]["AcroForm"][
                            "DR"
                        ],
                        name("Subtype"): name("Form"),
                        name("Type"): name("XObject"),
                        name("Filter"): name("FlateDecode"),
                        name("Length"): 19,
                    }
                )
            },
            name("DA"): f"{r} {g} {b} rg /{font_name} 12.000000 Tf",
            name("DR"): document["Trailer"]["Root"]["AcroForm"]["DR"],
            name("DV"): self.__default_value,
            name("F"): 4,
            name("Ff"): 0,
            name("FT"): name("Tx"),
            name("P"): document["Trailer"]["Root"],
            name("Rect"): [],
            name("Subtype"): name("Widget"),
            name("T"): self.__field_name
            or self._FormField__get_auto_generated_field_name(page),  # type: ignore[attr-defined]
            name("Type"): name("Annot"),
            name("V"): self.__value,
        }

        # append field to page /Annots
        if "Annots" not in page:
            page[name("Annots")] = []
        page[name("Annots")] += [self.__widget_dictionary]

        # append field to catalog
        document["Trailer"]["Root"]["AcroForm"]["Fields"].append(self.__widget_dictionary)  # type: ignore[call-overload, index, union-attr]

    #
    # PUBLIC
    #

    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        return (
            max(available_space[0], 64) if self.__max_size is None else self.__max_size,
            int(1.2 * self.__font_size)
            + self.get_padding_top()
            + self.get_padding_bottom(),
        )

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
        # init self._widget_dictionary
        # fmt: off
        self.__init_widget_dictionary(available_space=available_space, document=page.get_document(), page=page) # type: ignore[arg-type]
        # fmt: on

        # calculate where the background/borders need to be painted
        # fmt: off
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # BDC
        # fmt: off
        TextBox._begin_marked_content_with_dictionary(page=page, structure_element_type='Form')  # type: ignore[attr-defined]
        # fmt: on

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # calculate content x,y, width, height
        content_x: int = background_x + self.get_padding_left()
        content_y: int = background_y + self.get_padding_bottom()
        content_w: int = w - self.get_padding_right() - self.get_padding_left()
        content_h: int = h - self.get_padding_top() - self.get_padding_bottom()

        # set location
        # fmt: off
        if self.__widget_dictionary is not None:
            self.__widget_dictionary["AP"]["N"]["BBox"][2] = content_w  # type: ignore[call-overload, index]
            self.__widget_dictionary["AP"]["N"]["BBox"][3] = content_h  # type: ignore[call-overload, index]
            self.__widget_dictionary["Rect"] = [content_x,
                                               content_y,
                                               content_x + content_w,
                                               content_y + content_h]
