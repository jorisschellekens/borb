#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a checkbox form element in a PDF document.

The `CheckBox` class is used to create and manage checkbox fields within PDF forms.
Checkboxes allow users to make binary choices, typically represented as checked or
unchecked. This class facilitates the configuration and rendering of checkbox elements
in interactive PDF forms.
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
from borb.pdf.primitives import name, stream, PDFType


class CheckBox(FormField):
    """
    Represents a checkbox form element in a PDF document.

    The `CheckBox` class is used to create and manage checkbox fields within PDF forms.
    Checkboxes allow users to make binary choices, typically represented as checked or
    unchecked. This class facilitates the configuration and rendering of checkbox elements
    in interactive PDF forms.
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
        default_value: bool = False,
        field_name: typing.Optional[str] = None,
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
        value: bool = False,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a CheckBox form field, representing a selectable checkbox in a PDF form.

        :param background_color: Background color of the checkbox area.
        :param border_color: Border color for the checkbox.
        :param border_dash_pattern: Dash pattern for the checkbox border.
        :param border_dash_phase: Starting phase for the dashed border.
        :param border_width_bottom: Width of the bottom border.
        :param border_width_left: Width of the left border.
        :param border_width_right: Width of the right border.
        :param border_width_top: Width of the top border.
        :param default_value: Default checked state of the checkbox.
        :param field_name: Name assigned to the checkbox form field.
        :param horizontal_alignment: Horizontal alignment within the layout.
        :param margin_bottom: Bottom margin for spacing.
        :param margin_left: Left margin for spacing.
        :param margin_right: Right margin for spacing.
        :param margin_top: Top margin for spacing.
        :param padding_bottom: Bottom padding inside the checkbox.
        :param padding_left: Left padding inside the checkbox.
        :param padding_right: Right padding inside the checkbox.
        :param padding_top: Top padding inside the checkbox.
        :param value: Current checked state of the checkbox.
        :param vertical_alignment: Vertical alignment within the layout.
        """
        assert (
            field_name is None or len(field_name) > 0
        ), "The field_name must be None or a non-empty str."
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
        self.__value: bool = value
        self.__default_value: bool = default_value
        self.__field_name: typing.Optional[str] = field_name
        self.__font_size: int = font_size
        self.__font_color: Color = X11Color.BLACK
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
        font_name: name = self._FormField__get_font_resource_name(font=Standard14Fonts.get("Zapfdingbats"), page=page) # type: ignore[arg-type, attr-defined]
        # fmt: on

        # TODO
        self.__widget_dictionary = {
            name("AP"): {
                name("N"): {
                    name("Off"): stream(
                        {
                            name("BBox"): [
                                0,
                                0,
                                available_space[2],
                                available_space[3],
                            ],
                            name(
                                "Bytes"
                            ): b"x\x9c\xd3\x0f\xa9Pp\xf2u\xe6r\x05b\x00\x14&\x02\xd7",
                            name("Filter"): name("FlateDecode"),
                            name("Length"): 18,
                            name("Resources"): document["Trailer"]["Root"]["AcroForm"][
                                "DR"
                            ],
                            name("Subtype"): name("Form"),
                            name("Type"): name("XObject"),
                        }
                    ),
                    name("Yes"): stream(
                        {
                            name(
                                "Bytes"
                            ): f"/Tx BMC\nq BT\n{r} {g} {b} rg /{font_name} {self.__font_size} Tf\n1 2 Td [<34>] TJ\nET\nQ\nEMC\n".encode(
                                "latin1"
                            ),
                            name("Length"): 67,
                            name("Type"): name("XObject"),
                            name("Subtype"): name("Form"),
                            name("BBox"): [
                                0,
                                0,
                                available_space[2],
                                available_space[3],
                            ],
                            name("Resources"): document["Trailer"]["Root"]["AcroForm"][
                                "DR"
                            ],
                        }
                    ),
                },
            },
            name("AS"): name("Off"),
            name("DA"): f"{r} {g} {b} rg /{font_name} 0 Tf",
            name("DR"): document["Trailer"]["Root"]["AcroForm"]["DR"],
            name("DV"): name("Off"),
            name("F"): 4,
            name("FT"): name("Btn"),
            name("MK"): 8,
            name("Rect"): [],
            name("StructParent"): 1,
            name("Subtype"): name("Widget"),
            name("T"): self.__field_name
            or self._FormField__get_auto_generated_field_name(page),  # type: ignore[attr-defined]
            name("Type"): name("Annot"),
            name("V"): name("Off"),
        }

        # append field to page /Annots
        if "Annots" not in page:
            page[name("Annots")] = [self.__widget_dictionary]

        # append field to catalog
        catalog: typing.Dict[str, PDFType] = document["Trailer"]["Root"]  # type: ignore[attr-defined]
        if "AcroForm" not in catalog:
            catalog[name("AcroForm")] = {
                name("Fields"): [],
                name("DR"): {name("Font"): page["Resources"]["Font"]},
                name("NeedAppearances"): True,
            }
        catalog["AcroForm"]["Fields"].append(self.__widget_dictionary)  # type: ignore[call-overload, index, union-attr]

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
            self.__font_size + self.get_padding_left() + self.get_padding_right(),
            self.__font_size + self.get_padding_top() + self.get_padding_bottom(),
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
        CheckBox._begin_marked_content_with_dictionary(page=page, structure_element_type='Form')  # type: ignore[attr-defined]
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
            self.__widget_dictionary["AP"]["N"]['Off']["BBox"][2] = content_w  # type: ignore[call-overload, index]
            self.__widget_dictionary["AP"]["N"]['Off']["BBox"][3] = content_h  # type: ignore[call-overload, index]
            self.__widget_dictionary["AP"]["N"]['Yes']["BBox"][2] = content_w  # type: ignore[call-overload, index]
            self.__widget_dictionary["AP"]["N"]['Yes']["BBox"][3] = content_h  # type: ignore[call-overload, index]
            self.__widget_dictionary["Rect"] = [content_x,
                                               content_y,
                                               content_x + content_w,
                                               content_y + content_h]

        # EMC
        CheckBox._end_marked_content(page=page)  # type: ignore[attr-defined]
