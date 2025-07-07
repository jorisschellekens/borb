#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a button form element in a PDF document.

The `Button` class is used to create interactive buttons within PDF forms,
allowing users to trigger specific actions, such as submitting the form,
resetting fields, or navigating to different sections of the document.
Buttons enhance user interactivity and improve the overall functionality
of PDF forms.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.form.form_field import FormField
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name, stream


class Button(FormField):
    """
    Represents a button form element in a PDF document.

    The `Button` class is used to create interactive buttons within PDF forms,
    allowing users to trigger specific actions, such as submitting the form,
    resetting fields, or navigating to different sections of the document.
    Buttons enhance user interactivity and improve the overall functionality
    of PDF forms.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
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
        padding_bottom: int = 7,
        padding_left: int = 7,
        padding_right: int = 7,
        padding_top: int = 7,
        value: str = "",
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a Button component, representing a button form field that can be inserted into a PDF document.

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
        assert (
            field_name is None or len(field_name) > 0
        ), "The field_name must be None or a non-empty str."
        assert font_size > 0, "The font_size must be a non-negative value."
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
        self.__text: str = text
        self.__value: str = value
        self.__default_value: str = default_value
        self.__font_size: int = font_size
        self.__field_name: typing.Optional[str] = field_name
        self.__font_color: Color = font_color
        self.__widget_dictionary: typing.Optional[typing.Dict[str, PDFType]] = None

    #
    # PRIVATE
    #

    def __get_auto_generated_field_name(self, page: Page) -> str:
        number_of_fields: int = len(page.get("AcroForm", {}))
        return f"field-{number_of_fields:03d}"

    def __get_font_resource_name(self, font: Font, page: Page):
        # create resources if needed
        if "Resources" not in page:
            page[name("Resources")] = {}
        if "Font" not in page["Resources"]:
            page["Resources"][name("Font")] = {}

        # IF the font is already present
        # THEN return that particular font
        font_resource_name = [
            k for k, v in page["Resources"]["Font"].items() if v == font
        ]
        if len(font_resource_name) > 0:
            return font_resource_name[0]

        # IF the font is not yet present
        # THEN create it
        font_index = len(page["Resources"]["Font"]) + 1
        page["Resources"]["Font"][name("F%d" % font_index)] = font
        return name("F%d" % font_index)

    def __init_widget_dictionary(
        self,
        available_space: typing.Tuple[int, int, int, int],
        document: Document,
        page: Page,
    ):
        if self.__widget_dictionary is not None:
            return

        # fmt: off
        font_name: name = self.__get_font_resource_name(font=Standard14Fonts.get("Helvetica"), page=page) # type: ignore[arg-type]
        # fmt: on

        # widget dictionary
        # fmt: off
        self.__widget_dictionary = {
            # name("P"): catalog,
            name("AA"): {name('D'): {name('Type'): name("Action"), name("S"): name("ResetForm")}},
            name('AP'): {
                name("N"): stream({
                    name("Bytes"): b"x\\xda\\xd3\\x0f\\xa9Pp\\xf2uVp\\xf5u\\x06\\x00\\x11\\xa7\\x02\\xe3",
                    name("Length"): 10,
                    name("Type"): name("XObject"),
                    name("Subtype"): name("Form"),
                    name("BBox"): [0, 0, 0, 0],
                    name("Filter"): name("FlateDecode"),
                    name("Resources"): {
                        name("ProcSet"): [name('PDF'), name('Text')],
                        name("Font"): {}
                    }
                })
            },
            name("DA"): f"0.23921 0.23921 0.23921 rg {font_name} {self.__font_size} Tf",
            name("DR"): {name("Font"): {
                font_name: {
                    name("BaseFont"): name("Helvetica"),
                    name("Encoding"): name("WinAnsiEncoding"),
                    name("Subtype"): name("Type1"),
                    name("Type"): name("Font"),
                }
            }
            },
            name("F"): 4,
            name("Ff"): 65536,
            name("FT"): name("Btn"),
            name("MK"): {name("BC"): [], name("BG"): [], name("CA"): '', },
            name("Q"): 1,
            name("Rect"): [0, 0, 0, 0],
            name("Subtype"): name("Widget"),
            name("T"): self.__field_name or self.__get_auto_generated_field_name(page),
            name("Type"): name("Annot"),
        }
        # fmt: on

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
        from borb.pdf.layout_element.text.chunk import Chunk

        return Chunk(
            text=self.__text,
            border_width_bottom=self.get_border_width_bottom(),
            border_width_left=self.get_border_width_left(),
            border_width_right=self.get_border_width_top(),
            border_width_top=self.get_border_width_top(),
            font_size=self.__font_size,
            margin_bottom=self.get_margin_bottom(),
            margin_left=self.get_margin_left(),
            margin_right=self.get_margin_right(),
            margin_top=self.get_margin_top(),
            padding_bottom=self.get_padding_bottom(),
            padding_left=self.get_padding_left(),
            padding_right=self.get_padding_right(),
            padding_top=self.get_padding_top(),
        ).get_size(available_space=available_space)

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

        # BDC
        # fmt: off
        Button._begin_marked_content_with_dictionary(page=page, structure_element_type='Form')  # type: ignore[attr-defined]
        # fmt: on

        # paint
        from borb.pdf.layout_element.text.chunk import Chunk

        chunk: Chunk = Chunk(
            text=self.__text,
            background_color=self.get_background_color(),
            border_color=self.get_border_color(),
            border_dash_pattern=self.get_border_dash_pattern(),
            border_dash_phase=self.get_border_dash_phase(),
            border_width_bottom=self.get_border_width_bottom(),
            border_width_left=self.get_border_width_left(),
            border_width_right=self.get_border_width_top(),
            border_width_top=self.get_border_width_top(),
            font_size=self.__font_size,
            horizontal_alignment=self.get_horizontal_alignment(),
            margin_bottom=self.get_margin_bottom(),
            margin_left=self.get_margin_left(),
            margin_right=self.get_margin_right(),
            margin_top=self.get_margin_top(),
            padding_bottom=self.get_padding_bottom(),
            padding_left=self.get_padding_left(),
            padding_right=self.get_padding_right(),
            padding_top=self.get_padding_top(),
            vertical_alignment=self.get_vertical_alignment(),
        )
        chunk.paint(available_space=available_space, page=page)

        # set location
        # fmt: off
        self._LayoutElement__previous_paint_box = chunk.get_previous_paint_box()
        assert self._LayoutElement__previous_paint_box is not None
        x, y, w, h = self._LayoutElement__previous_paint_box
        if self.__widget_dictionary is not None:
            self.__widget_dictionary["AP"]["N"]["BBox"][2] = w  # type: ignore[call-overload, index]
            self.__widget_dictionary["AP"]["N"]["BBox"][3] = h  # type: ignore[call-overload, index]
            self.__widget_dictionary["Rect"] = [x, y, x + w, y + h]
        # fmt: on

        # EMC
        Button._end_marked_content(page=page)  # type: ignore[attr-defined]
