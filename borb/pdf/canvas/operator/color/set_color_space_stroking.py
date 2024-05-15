#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(PDF 1.1) Set the current colour space to use for stroking operations. The
operand name shall be a name object. If the colour space is one that can
be specified by a name and no additional parameters (DeviceGray,
DeviceRGB, DeviceCMYK, and certain cases of Pattern), the name may
be specified directly. Otherwise, it shall be a name defined in the
ColorSpace subdictionary of the current resource dictionary (see 7.8.3,
"Resource Dictionaries"); the associated value shall be an array
describing the colour space (see 8.6.3, "Colour Space Families").

The names DeviceGray, DeviceRGB, DeviceCMYK, and Pattern
always identify the corresponding colour spaces directly; they never refer
to resources in the ColorSpace subdictionary.

The CS operator shall also set the current stroking colour to its initial
value, which depends on the colour space:
In a DeviceGray, DeviceRGB, CalGray, or CalRGB colour space, the
initial colour shall have all components equal to 0.0.
In a DeviceCMYK colour space, the initial colour shall be
[ 0.0 0.0 0.0 1.0 ].

In a Lab or ICCBased colour space, the initial colour shall have all
components equal to 0.0 unless that falls outside the intervals specified
by the space’s Range entry, in which case the nearest valid value shall be
substituted.

In an Indexed colour space, the initial colour value shall be 0.
In a Separation or DeviceN colour space, the initial tint value shall be 1.0
for all colorants.
In a Pattern colour space, the initial colour shall be a pattern object that
causes nothing to be painted.
"""
import logging
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import CMYKColor
from borb.pdf.canvas.color.color import GrayColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.color.color import Separation
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator

logger = logging.getLogger(__name__)


class SetColorSpaceStroking(CanvasOperator):
    """
    (PDF 1.1) Set the current colour space to use for stroking operations. The
    operand name shall be a name object. If the colour space is one that can
    be specified by a name and no additional parameters (DeviceGray,
    DeviceRGB, DeviceCMYK, and certain cases of Pattern), the name may
    be specified directly. Otherwise, it shall be a name defined in the
    ColorSpace subdictionary of the current resource dictionary (see 7.8.3,
    "Resource Dictionaries"); the associated value shall be an array
    describing the colour space (see 8.6.3, "Colour Space Families").

    The names DeviceGray, DeviceRGB, DeviceCMYK, and Pattern
    always identify the corresponding colour spaces directly; they never refer
    to resources in the ColorSpace subdictionary.

    The CS operator shall also set the current stroking colour to its initial
    value, which depends on the colour space:
    In a DeviceGray, DeviceRGB, CalGray, or CalRGB colour space, the
    initial colour shall have all components equal to 0.0.
    In a DeviceCMYK colour space, the initial colour shall be
    [ 0.0 0.0 0.0 1.0 ].

    In a Lab or ICCBased colour space, the initial colour shall have all
    components equal to 0.0 unless that falls outside the intervals specified
    by the space’s Range entry, in which case the nearest valid value shall be
    substituted.

    In an Indexed colour space, the initial colour value shall be 0.
    In a Separation or DeviceN colour space, the initial tint value shall be 1.0
    for all colorants. In a Pattern colour space, the initial colour shall be a pattern object that
    causes nothing to be painted.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("CS", 1)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the CS operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """

        assert isinstance(operands[0], Name)
        color_space_name: Name = operands[0]
        color_space: typing.List = []

        if color_space_name not in [
            "DeviceGray",
            "DeviceRGB",
            "DeviceCMYK",
            "CalGray",
            "CalRGB",
            "Lab",
            "ICCBased",
            "Indexed",
            "Pattern",
            "Separation",
        ]:
            color_space_name = canvas_stream_processor.get_resource(
                "ColorSpace", color_space_name
            )

        if not isinstance(color_space_name, Name) and isinstance(
            color_space_name, typing.List
        ):
            assert isinstance(color_space_name[0], Name)
            color_space = color_space_name
            color_space_name = color_space_name[0]

        #
        # Device
        #
        canvas = canvas_stream_processor.get_canvas()
        if color_space_name == "DeviceGray":
            canvas.graphics_state.stroke_color_space = color_space_name
            canvas.graphics_state.stroke_color = GrayColor(Decimal(0))
            return
        if color_space_name == "DeviceRGB":
            canvas.graphics_state.stroke_color_space = color_space_name
            canvas.graphics_state.stroke_color = RGBColor(
                Decimal(0), Decimal(0), Decimal(0)
            )
            return
        if color_space_name == "DeviceCMYK":
            canvas.graphics_state.stroke_color_space = color_space_name
            canvas.graphics_state.stroke_color = CMYKColor(
                Decimal(0), Decimal(0), Decimal(0), Decimal(1)
            )
            return

        #
        # CIE-based
        #

        if color_space_name == "CalGray":
            canvas.graphics_state.stroke_color_space = color_space_name
            canvas.graphics_state.stroke_color = GrayColor(Decimal(0))
            return
        if color_space_name == "CalRGB":
            canvas.graphics_state.stroke_color_space = color_space_name
            canvas.graphics_state.stroke_color = RGBColor(
                Decimal(0), Decimal(0), Decimal(0)
            )
            return
        if color_space_name == "Lab":
            canvas.graphics_state.stroke_color_space = color_space_name
            return
        if color_space_name == "ICCBased":
            canvas.graphics_state.stroke_color_space = color_space_name
            canvas.graphics_state.stroke_color = RGBColor(
                Decimal(0), Decimal(0), Decimal(0)
            )
            return

        #
        # Special
        #
        if color_space_name == "Indexed":
            canvas.graphics_state.stroke_color_space = color_space_name
            return
        if color_space_name == "Pattern":
            canvas.graphics_state.stroke_color_space = operands[0]
            return
        if color_space_name == "Separation":
            canvas.graphics_state.stroke_color_space = color_space
            canvas.graphics_state.stroke_color = Separation(color_space, [Decimal(0)])
