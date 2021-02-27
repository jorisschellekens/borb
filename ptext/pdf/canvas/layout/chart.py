import io
from decimal import Decimal
from typing import Optional

import matplotlib.pyplot as MatPlotLibPlot  # type: ignore [import]
from PIL import Image as PILImage  # type: ignore [import]

from ptext.pdf.canvas.layout.image import Image


class Chart(Image):
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
