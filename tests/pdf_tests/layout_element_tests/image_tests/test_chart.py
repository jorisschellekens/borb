import math
import typing

import matplotlib  # type: ignore[import-not-found]
import matplotlib.pyplot as plt  # type: ignore[import-not-found]

from borb.pdf.document import Document
from borb.pdf.layout_element.image.chart import Chart
from borb.pdf.page import Page
from tests.test_case import TestCase


class TestChart(TestCase):

    @staticmethod
    def _create_matplotlib_pyplot() -> typing.Any:

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

    def test_chart_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Chart(
            matplotlib_plt=TestChart._create_matplotlib_pyplot(),
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(what=d, where_to="test_chart_001.pdf")

    def test_chart_002(self):
        import numpy as np  # type: ignore[import-untyped]
        import pandas as pd  # type: ignore[import-untyped]

        day_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        time_order = ["Night", "Morning", "Midday", "Evening"]
        matrix = np.array(
            [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [8, 9, 8, 9],
                [9, 6, 4, 3],
                [2, 3, 2, 3],
                [1, 0, 0, 4],
                [5, 4, 3, 4],
            ]
        )

        # convert to heatmap dataframe
        df_heat = pd.DataFrame(matrix, index=day_order, columns=time_order)

        import matplotlib.pyplot as plt

        print(matplotlib.__version__)
        plt.figure(figsize=(8, 4))
        plt.imshow(df_heat.values, aspect="auto")
        plt.xticks(range(len(df_heat.columns)), df_heat.columns)
        plt.yticks(range(len(df_heat.index)), df_heat.index)
        plt.colorbar(label="Number of incidents")
        plt.title("Incidents by Day and Time Block")
        plt.xlabel("Time of day")
        plt.ylabel("Day of week")
        plt.show()

        from borb.pdf import Document
        from borb.pdf import Page
        from borb.pdf import PageLayout
        from borb.pdf import SingleColumnLayout
        from borb.pdf import Chart

        pdf_document: Document = Document()

        page: Page = Page()
        pdf_document.append_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)
        page_layout.append_layout_element(Chart(plt.gcf(), size=(100, 100)))

        TestCase.write(what=pdf_document, where_to="test_chart_002.pdf")
