#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'scn' operator: Set the color for nonstroking operations in special color spaces (ICCBased, Separation, DeviceN, and Pattern).

This operator sets the current color for nonstroking operations in advanced color spaces, including ICCBased,
Separation, DeviceN, and Pattern. The number and interpretation of the operands depend on the current nonstroking
color space:

- For Separation, DeviceN, or ICCBased color spaces, the operands (c1...cn) are numbers that specify the
  color components.
- For Pattern color spaces, the first operand is a name (representing an entry in the Pattern subdictionary of the
  current resource dictionary). If the pattern is uncolored (PatternType = 1 and PaintType = 2), additional operands
  specify the color in the pattern’s underlying color space.

The 'scn' operator updates the nonstroking color in the current graphics state and is used for filling paths,
shapes, or any other graphical elements that require special color handling.

Note:
    - The 'scn' operator is versatile and supports color spaces beyond the standard Device color spaces (RGB, CMYK, and Gray).
    - For stroking operations in these advanced color spaces, use the 'SCN' operator.
"""

import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorscn(Operator):
    """
    The 'scn' operator: Set the color for nonstroking operations in special color spaces (ICCBased, Separation, DeviceN, and Pattern).

    This operator sets the current color for nonstroking operations in advanced color spaces, including ICCBased,
    Separation, DeviceN, and Pattern. The number and interpretation of the operands depend on the current nonstroking
    color space:

    - For Separation, DeviceN, or ICCBased color spaces, the operands (c1...cn) are numbers that specify the
      color components.
    - For Pattern color spaces, the first operand is a name (representing an entry in the Pattern subdictionary of the
      current resource dictionary). If the pattern is uncolored (PatternType = 1 and PaintType = 2), additional operands
      specify the color in the pattern’s underlying color space.

    The 'scn' operator updates the nonstroking color in the current graphics state and is used for filling paths,
    shapes, or any other graphical elements that require special color handling.

    Note:
        - The 'scn' operator is versatile and supports color spaces beyond the standard Device color spaces (RGB, CMYK, and Gray).
        - For stroking operations in these advanced color spaces, use the 'SCN' operator.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, source: Source):
        """
        Initialize the 'scn' operator.

        This operator requires access to the active rendering Source because
        the number and interpretation of operands depend on the currently
        selected non-stroking color space in the graphics state.

        The Source instance provides access to:
        - The current graphics state
        - The active non-stroking color space
        - Validation context for operand count and color component semantics

        Since the 'scn' operator does not explicitly specify a color space
        (it uses the one already set in the graphics state), it must query
        the Source at execution time to determine how many operands are
        expected (e.g., 1 for DeviceGray, 3 for DeviceRGB, 4 for DeviceCMYK,
        or a color-space-defined component count for other spaces).

        :param source: The Source representing the page/content stream
                       currently being rendered. It provides access to
                       the graphics state, including the active
                       non-stroking color space.
        """
        self.__source = source

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def apply(
        self,
        operands: typing.List[PDFType],
        page: Page,
        source: Source,
    ) -> None:
        """
        Apply the operator's logic to the given `Page`.

        This method executes the operator using the provided operands, applying its
        effects to the specified `Page` via the `Source` processor. Subclasses should
        override this method to implement specific operator behavior.

        :param page: The `Page` object to which the operator is applied.
        :param source: The `Source` object managing the content stream.
        :param operands: A list of `PDFType` objects representing the operator's operands.
        """
        from borb.pdf.color.grayscale_color import GrayscaleColor
        from borb.pdf.color.rgb_color import RGBColor
        from borb.pdf.color.cmyk_color import CMYKColor

        if self.__source.non_stroke_color_space == "CalGray":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            self.__source.non_stroke_color = GrayscaleColor(level=operands[0])
        if self.__source.non_stroke_color_space == "CalRGB":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            assert isinstance(operands[1], int) or isinstance(operands[1], float)
            assert isinstance(operands[2], int) or isinstance(operands[2], float)
            self.__source.non_stroke_color = RGBColor(
                red=int(operands[0] * 255),
                green=int(operands[1] * 255),
                blue=int(operands[2] * 255),
            )
        if self.__source.non_stroke_color_space == "DeviceCMYK":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            assert isinstance(operands[1], int) or isinstance(operands[1], float)
            assert isinstance(operands[2], int) or isinstance(operands[2], float)
            assert isinstance(operands[3], int) or isinstance(operands[3], float)
            self.__source.non_stroke_color = CMYKColor(
                cyan=operands[0],
                magenta=operands[1],
                yellow=operands[2],
                key=operands[3],
            )
        if self.__source.non_stroke_color_space == "DeviceGray":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            self.__source.non_stroke_color = GrayscaleColor(level=operands[0])
        if self.__source.non_stroke_color_space == "DeviceRGB":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            assert isinstance(operands[1], int) or isinstance(operands[1], float)
            assert isinstance(operands[2], int) or isinstance(operands[2], float)
            self.__source.non_stroke_color = RGBColor(
                red=int(operands[0] * 255),
                green=int(operands[1] * 255),
                blue=int(operands[2] * 255),
            )
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "scn"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        if self.__source.non_stroke_color_space == "CalGray":
            return 1
        if self.__source.non_stroke_color_space == "CalRGB":
            return 3
        if self.__source.non_stroke_color_space == "DeviceCMYK":
            return 4
        if self.__source.non_stroke_color_space == "DeviceGray":
            return 1
        if self.__source.non_stroke_color_space == "DeviceRGB":
            return 3
        # TODO
        return 0
