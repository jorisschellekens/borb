#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents a Chart
"""
import io
import typing
from decimal import Decimal
from typing import Optional

import matplotlib.pyplot as MatPlotLibPlot  # type: ignore [import]
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from PIL import Image as PILImage  # type: ignore [import]


class Chart(Image):
    """
    This implementation of LayoutElement represents a Chart
    """

    def __init__(
        self,
        chart: MatPlotLibPlot,
        width: Optional[Decimal] = None,
        height: Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        byte_buffer = io.BytesIO()
        chart.savefig(byte_buffer, format="png")
        byte_buffer.seek(0)

        super(Chart, self).__init__(
            image=PILImage.open(byte_buffer),
            width=width,
            height=height,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )
