#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a sequence of characters on a single line.

Chunks correspond to continuous text that does not wrap across multiple lines. The text
in a `Chunk` starts and ends within the same line in a PDF document, making it the
smallest unit of text within a layout.
"""

import functools
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.helvetica.helvetica import Helvetica
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name


class Chunk(LayoutElement):
    """
    Represents a sequence of characters on a single line.

    Chunks correspond to continuous text that does not wrap across multiple lines. The text
    in a `Chunk` starts and ends within the same line in a PDF document, making it the
    smallest unit of text within a layout.
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
        font: typing.Optional[typing.Union[Font, str]] = None,
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
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
        word_spacing: float = 0,
    ):
        """
        Initialize a Chunk object representing a segment of text.

        The `Chunk` class encapsulates a chunk of text with customizable properties such as background color,
        font, font size, and alignment.

        :param text:                    The text content of the chunk.
        :param background_color:        The background color of the chunk. Defaults to None.
        :param font:                    The font used for the text. Defaults to None.
        :param font_color:              The color of the font. Defaults to X11Color.BLACK.
        :param font_size:               The size of the font in points. Defaults to 12.
        :param border_color:            The color of the border around the chunk. Defaults to None.
        :param border_dash_pattern:     A list defining the dash pattern for the border. Defaults to an empty list.
        :param border_dash_phase:       The phase of the dash pattern. Defaults to 0.
        :param border_width_bottom:     Width of the bottom border in pixels. Defaults to 0.
        :param border_width_left:       Width of the left border in pixels. Defaults to 0.
        :param border_width_right:      Width of the right border in pixels. Defaults to 0.
        :param border_width_top:        Width of the top border in pixels. Defaults to 0.
        :param horizontal_alignment:    Horizontal alignment of the text within the chunk. Defaults to LayoutElement.HorizontalAlignment.LEFT.
        :param margin_bottom:           Bottom margin in pixels. Defaults to 0.
        :param margin_left:             Left margin in pixels. Defaults to 0.
        :param margin_right:            Right margin in pixels. Defaults to 0.
        :param margin_top:              Top margin in pixels. Defaults to 0.
        :param padding_bottom:          Bottom padding in pixels. Defaults to 0.
        :param padding_left:            Left padding in pixels. Defaults to 0.
        :param padding_right:           Right padding in pixels. Defaults to 0.
        :param padding_top:             Top padding in pixels. Defaults to 0.
        :param vertical_alignment:      Vertical alignment of the text within the chunk. Defaults to LayoutElement.VerticalAlignment.BOTTOM.
        """
        super().__init__(
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
        assert font_size > 0
        assert character_spacing >= 0
        assert word_spacing >= 0
        self.__character_spacing: float = character_spacing
        if isinstance(font, str):
            font = Standard14Fonts.get(font)
            assert font is not None
        self.__font: Font = font or Helvetica()
        self.__font_color: Color = font_color
        self.__font_size: int = font_size
        self.__text: str = text
        self.__word_spacing: float = word_spacing

    #
    # PRIVATE
    #

    @staticmethod
    def __cmp_font_dictionaries(f0: Font, f1: Font) -> bool:
        for key in f0.keys() | f1.keys():
            if key == "Name":
                continue
            if f0.get(key, None) != f1.get(key, None):
                return False
        return True

    @staticmethod
    def __escape_special_chars_in_ascii_mode(s: str) -> str:
        sOut: str = ""
        for c in s:
            if c == "\r":
                sOut += "\\r"
            elif c == "\n":
                sOut += "\\n"
            elif c == "\t":
                sOut += "\\t"
            elif c == "\b":
                sOut += "\\b"
            elif c == "\f":
                sOut += "\\f"
            elif c in ["(", ")", "\\"]:
                sOut += "\\" + c
            elif 0 <= ord(c) < 8:
                sOut += "\\00" + oct(ord(c))[2:]
            elif 8 <= ord(c) < 32:
                sOut += "\\0" + oct(ord(c))[2:]
            else:
                sOut += c
        return sOut

    @staticmethod
    def __escape_special_chars_in_hex_mode(font: Font, s: str) -> str:

        # IF the font uses Identity-H OR Identity-V encoding
        # THEN use four bytes
        number_of_bytes_per_char: int = 2
        if "Encoding" in font and font["Encoding"] in ["Identity-H", "Identity-V"]:
            number_of_bytes_per_char = 4

        # decode each character
        s2: str = ""
        for c in s:
            c1: int = font.get_character_code(c)
            if c1 is None or c1 == -1:
                assert False, f"Font {font['BaseFont']} can not represent {c}"
            c2 = hex(c1)[2:]

            # apply padding to each hex sequence
            while len(c2) < number_of_bytes_per_char:
                c2 = "0" + c2

            # add the angle brackets
            c2 = "<" + c2 + ">"

            # append to the string
            s2 += c2

        # return
        return s2

    #
    # PUBLIC
    #

    def get_character_spacing(self) -> float:
        """
        Retrieve the character spacing for this chunk of text.

        Character spacing determines the additional space added between characters in the text.
        It is specified as an unscaled value, meaning it will later be multiplied by the font size
        to compute the final spacing. A character spacing of `0` (the default) means no extra spacing
        is added, while a value of `1` adds an extra space equal to the font size (in ems) to the
        width of each character.

        :return: The unscaled character spacing as a float.
        """
        return self.__character_spacing

    def get_font(self) -> "Font":
        """
        Return the font used for the text chunk.

        This method returns the font object associated with the text chunk,
        which defines the typography and style of the rendered text.

        :return: The font object associated with this Chunk
        """
        return self.__font

    def get_font_color(self) -> Color:
        """
        Return the font color used for the text chunk.

        This method returns the color object associated with the text chunk,
        which determines the color of the rendered text.

        :return: The color object associated with this Chunk
        """
        return self.__font_color

    def get_font_size(self) -> int:
        """
        Return the font size used for the text chunk.

        This method returns the font size associated with the text chunk.

        :return: The font size associated with this Chunk
        """
        return self.__font_size

    @functools.cache
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
        w: int = self.__font.get_width(
            font_size=self.__font_size,
            text=self.__text,
            character_spacing=self.__character_spacing,
            word_spacing=self.__word_spacing,
        )
        h: int = self.__font_size
        return (
            w + self.get_padding_bottom() + self.get_padding_right(),
            h + self.get_padding_bottom() + self.get_padding_top(),
        )

    def get_text(self) -> str:
        """
        Return the text associated with the text chunk.

        This method returns the string content that is stored within the text chunk.

        :return: The text associated with this Chunk
        """
        return self.__text

    def get_word_spacing(self) -> float:
        """
        Retrieve the word spacing for this chunk of text.

        Word spacing specifies the additional space added to each space character in the text.
        It is defined as an unscaled value, which will later be multiplied by the font size to
        determine the final spacing. A default value of `0` means no extra space is added, while
        a positive value increases the spacing for each space character.

        :return: The unscaled word spacing as a float.
        """
        return self.__word_spacing

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
        # resources
        if "Resources" not in page:
            page["Resources"] = {}
        if "Font" not in page["Resources"]:
            page["Resources"]["Font"] = {}

        # create new font_name
        font_name: typing.Optional[str] = next(
            iter(
                [
                    k
                    for k, v in page["Resources"]["Font"].items()
                    if Chunk.__cmp_font_dictionaries(v, self.__font)
                ]
            ),
            None,
        )
        if font_name is None:
            font_name = "F1"
            while font_name in page["Resources"]["Font"]:
                font_name = f"F{int(font_name[1:]) + 1}"
            self.__font["Name"] = name(font_name)
            page["Resources"]["Font"][font_name] = self.__font

        # calculate width and height
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

        # calculate where the background/borders need to be painted
        # fmt: off
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

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # leading newline (if needed)
        Chunk._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # character spacing
        if self.__character_spacing != 0:
            page["Contents"][
                "DecodedBytes"
            ] += f"{self.__character_spacing} Tc\n".encode("latin1")

        # word spacing
        if self.__word_spacing != 0:
            page["Contents"]["DecodedBytes"] += f"{self.__word_spacing} Tw\n".encode(
                "latin1"
            )

        # begin text
        page["Contents"]["DecodedBytes"] += b"BT\n"

        # set font_color
        rgb_font_color: RGBColor = self.__font_color.to_rgb_color()
        page["Contents"]["DecodedBytes"] += (
            f"{round(rgb_font_color.get_red() / 255, 7)} "
            f"{round(rgb_font_color.get_green() / 255, 7)} "
            f"{round(rgb_font_color.get_blue() / 255, 7)} rg\n"
        ).encode("latin1")

        # apply font, font_size
        page["Contents"]["DecodedBytes"] += f"/{font_name} 1 Tf\n".encode("latin1")

        # move to position
        page["Contents"]["DecodedBytes"] += (
            f"{self.__font_size} 0 "
            f"0 {self.__font_size} "
            f"{background_x + self.get_padding_left()} {background_y + self.get_padding_bottom()} Tm\n"
        ).encode("latin1")

        # write text
        from borb.pdf.font.simple_font.symbol.symbol import Symbol
        from borb.pdf.font.simple_font.zapfdingbats.zapfdingbats import ZapfDingbats
        from borb.pdf.font.simple_font.standard_type_1_font import StandardType1Font

        if isinstance(self.__font, Symbol) or isinstance(self.__font, ZapfDingbats):
            tj_arg: str = Chunk.__escape_special_chars_in_hex_mode(
                font=self.__font, s=self.__text
            )
            page["Contents"]["DecodedBytes"] += f"[{tj_arg}] TJ\n".encode("latin1")

        elif isinstance(self.__font, StandardType1Font):
            tj_arg = Chunk.__escape_special_chars_in_ascii_mode(self.__text)  # type: ignore[no-redef]
            page["Contents"]["DecodedBytes"] += f"({tj_arg}) Tj\n".encode("latin1")

        else:
            tj_arg = Chunk.__escape_special_chars_in_hex_mode(
                font=self.__font, s=self.__text
            )
            page["Contents"]["DecodedBytes"] += f"[{tj_arg}] TJ\n".encode("latin1")

        # end text
        page["Contents"]["DecodedBytes"] += b"ET\n"

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"
