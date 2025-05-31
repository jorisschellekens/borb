#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'CS' operator: Set the current colour space for stroking operations.

The 'CS' operator is used to set the current colour space for stroking operations in a PDF content stream.
The operand for this operator is a name object that specifies the colour space. If the colour space is one
of the predefined ones, such as DeviceGray, DeviceRGB, DeviceCMYK, or certain cases of Pattern, the name may
be specified directly. Otherwise, the name corresponds to an entry in the ColorSpace subdictionary of the
current resource dictionary, where the associated value describes the colour space.

The operator also resets the current stroking colour to its initial value, which depends on the chosen colour space:
    - For DeviceGray, DeviceRGB, CalGray, or CalRGB, the initial colour has all components equal to 0.0.
    - For DeviceCMYK, the initial colour is [0.0, 0.0, 0.0, 1.0].
    - For Lab or ICCBased colour spaces, the initial colour components are set to 0.0, unless that falls outside
      the defined range, in which case the nearest valid value is used.
    - For Indexed colour spaces, the initial colour is set to 0.
    - For Separation or DeviceN colour spaces, the initial tint value is 1.0 for all colorants.
    - For Pattern colour spaces, the initial colour is a pattern object that causes nothing to be painted.

Note:
    For more details on colour spaces and the initial colour values, refer to PDF specification section 7.8.3,
    "Resource Dictionaries," and section 8.6.3, "Colour Space Families."
"""
import typing

from borb.pdf.color.x11_color import X11Color
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorCS(Operator):
    """
    The 'CS' operator: Set the current colour space for stroking operations.

    The 'CS' operator is used to set the current colour space for stroking operations in a PDF content stream.
    The operand for this operator is a name object that specifies the colour space. If the colour space is one
    of the predefined ones, such as DeviceGray, DeviceRGB, DeviceCMYK, or certain cases of Pattern, the name may
    be specified directly. Otherwise, the name corresponds to an entry in the ColorSpace subdictionary of the
    current resource dictionary, where the associated value describes the colour space.

    The operator also resets the current stroking colour to its initial value, which depends on the chosen colour space:
        - For DeviceGray, DeviceRGB, CalGray, or CalRGB, the initial colour has all components equal to 0.0.
        - For DeviceCMYK, the initial colour is [0.0, 0.0, 0.0, 1.0].
        - For Lab or ICCBased colour spaces, the initial colour components are set to 0.0, unless that falls outside
          the defined range, in which case the nearest valid value is used.
        - For Indexed colour spaces, the initial colour is set to 0.
        - For Separation or DeviceN colour spaces, the initial tint value is 1.0 for all colorants.
        - For Pattern colour spaces, the initial colour is a pattern object that causes nothing to be painted.

    Note:
        For more details on colour spaces and the initial colour values, refer to PDF specification section 7.8.3,
        "Resource Dictionaries," and section 8.6.3, "Colour Space Families."
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
        assert isinstance(operands[0], name)
        source.stroke_color_space = operands[0]
        if operands[0] in ["DeviceGray", "DeviceRGB", "CalGray", "CalRGB"]:
            self.stroke_color = X11Color.BLACK
            return
        if operands[0] in ["DeviceCMYK"]:
            self.stroke_color = X11Color.BLACK
            return
        if operands[0] in ["Lab"]:
            # TODO
            self.stroke_color = X11Color.BLACK
            return
        if operands[0] in ["ICCBased"]:
            # TODO
            self.stroke_color = X11Color.BLACK
            return
        if operands[0] in ["Indexed"]:
            # TODO
            self.stroke_color = X11Color.BLACK
            return
        if operands[0] in ["Separation", "DeviceN"]:
            # TODO
            self.stroke_color = X11Color.BLACK
            return
        if operands[0] in ["Pattern"]:
            # TODO
            self.stroke_color = X11Color.BLACK
            return
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "CS"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
