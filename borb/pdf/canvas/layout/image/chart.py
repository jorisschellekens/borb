#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents a Chart
"""
import io
from decimal import Decimal
from typing import Optional

import matplotlib.pyplot as MatPlotLibPlot  # type: ignore [import]
from PIL import Image as PILImage  # type: ignore [import]

from borb.pdf.canvas.layout.image.image import Image


class Chart(Image):
    """
    This implementation of LayoutElement represents a Chart
    """

    def __init__(
        self,
        chart: MatPlotLibPlot,
        width: Optional[Decimal] = None,
        height: Optional[Decimal] = None,
    ):
        byte_buffer = io.BytesIO()
        chart.savefig(byte_buffer, format="png")
        byte_buffer.seek(0)

        super(Chart, self).__init__(
            image=PILImage.open(byte_buffer), width=width, height=height
        )
