#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents a Chart
"""
import io
import logging
import typing
from decimal import Decimal

from PIL import Image as PILImageModule

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment

logger = logging.getLogger(__name__)


class Chart(Image):
    """
    This implementation of LayoutElement represents a Chart
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        chart: "matplotlib.pyplot",  # type: ignore[name-defined]
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        height: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
        width: typing.Optional[Decimal] = None,
    ):
        # try setting the dpi
        try:
            chart.dpi = max(600, chart.dpi)
        except:
            logger.info(
                "Unable to set matplotlib.pyplot.dpi, the Chart may be low-res."
            )
            pass

        # chart to image
        byte_buffer = io.BytesIO()
        chart.savefig(byte_buffer, format="png")
        byte_buffer.seek(0)

        super(Chart, self).__init__(
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            height=height,
            horizontal_alignment=horizontal_alignment,
            image=PILImageModule.open(byte_buffer),
            margin_bottom=margin_bottom if margin_bottom is not None else Decimal(5),
            margin_left=margin_left if margin_left is not None else Decimal(5),
            margin_right=margin_right if margin_right is not None else Decimal(5),
            margin_top=margin_top if margin_top is not None else Decimal(5),
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
            width=width,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
