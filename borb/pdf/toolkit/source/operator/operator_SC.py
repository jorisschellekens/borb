#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'SC' operator: Set the color for stroking operations in a device, CIE-based, or Indexed color space.

This operator sets the color to use for stroking paths, depending on the current
stroking color space. The number of operands required and their interpretation
varies based on the specific color space in use:

- For DeviceGray, CalGray, and Indexed color spaces, one operand is required.
- For DeviceRGB, CalRGB, and Lab color spaces, three operands are required.
- For DeviceCMYK color space, four operands are required.

The operands represent the components of the color in the corresponding color space.
For example, in DeviceRGB, the three operands represent the red, green, and blue components.

Note:
    This operator applies only to stroking operations and will not affect non-stroking
    color or other graphics state parameters.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorSC(Operator):
    """
    The 'SC' operator: Set the color for stroking operations in a device, CIE-based, or Indexed color space.

    This operator sets the color to use for stroking paths, depending on the current
    stroking color space. The number of operands required and their interpretation
    varies based on the specific color space in use:

    - For DeviceGray, CalGray, and Indexed color spaces, one operand is required.
    - For DeviceRGB, CalRGB, and Lab color spaces, three operands are required.
    - For DeviceCMYK color space, four operands are required.

    The operands represent the components of the color in the corresponding color space.
    For example, in DeviceRGB, the three operands represent the red, green, and blue components.

    Note:
        This operator applies only to stroking operations and will not affect non-stroking
        color or other graphics state parameters.
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
        # TODO
        if source.stroke_color_space in [
            "DeviceGray",
            "CalRGB",
            "Indexed",
        ]:
            pass
        if source.stroke_color_space in [
            "DeviceRGB",
            "CalRGB",
            "Lab",
        ]:
            pass
        if source.stroke_color_space in ["DeviceCMYK"]:
            pass
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "SC"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        # TODO
        return 0
