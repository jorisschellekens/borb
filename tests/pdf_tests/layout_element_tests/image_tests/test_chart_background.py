import math
import unittest

import matplotlib
import matplotlib.pyplot as plt

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.chart import Chart
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestChartBackground(unittest.TestCase):

    @staticmethod
    def _create_matplotlib_pyplot() -> matplotlib.pyplot:

        # Data for the plot
        x = [i for i in range(0, 360, 5)]
        y = [math.sin(math.radians(x)) * 10 for x in x]

        # Create the plot
        plt.plot(x, y, marker="o", linestyle="-", color="b", label="y = x^2")

        # Add labels and title
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Simple Plot of y = sin(x) * 10")

        # return
        return plt

    def test_chart_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Chart(
            matplotlib_plt=TestChartBackground._create_matplotlib_pyplot(),
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(80, 80),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_chart_background.pdf")
