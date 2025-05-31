import math
import typing
import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.visitor.pdf import PDF


class TestAllFlowchartShapes(unittest.TestCase):

    def test_all_flowchart_shapes(self):

        flowchart_methods = []
        for name, method in LineArt.__dict__.items():
            if not name.startswith("flowchart_"):
                continue
            flowchart_methods += [(name, method)]

        number_of_rows: int = math.floor(math.sqrt(len(flowchart_methods)))
        number_of_columns: int = math.ceil(len(flowchart_methods) / number_of_rows)

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        table: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_rows=number_of_rows * 2, number_of_columns=number_of_columns
        )

        # append each flowchart Shape
        flowchart_methods.sort(key=lambda x: x[0])

        while len(flowchart_methods) > 0:

            # produce names
            K: int = min(number_of_columns, len(flowchart_methods))
            for i in range(0, K):
                name: str = flowchart_methods[i][0]
                name = name.replace("flowchart_", "")
                name = name.replace("_", " ")
                table.append_layout_element(
                    Paragraph(
                        name,
                        font_size=8,
                        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                        text_alignment=LayoutElement.TextAlignment.CENTERED,
                    )
                )
            for i in range(0, number_of_columns - K):
                table.append_layout_element(Paragraph("", font_size=8))

            # produce shapes
            for i in range(0, K):
                v = flowchart_methods[i][1]
                shape: typing.Optional[Shape] = v(fill_color=X11Color.YELLOW_MUNSELL)
                if shape is not None:
                    shape._LayoutElement__horizontal_alignment = (
                        LayoutElement.HorizontalAlignment.MIDDLE
                    )
                    table.append_layout_element(shape.scale_to_fit(size=(40, 40)))
                else:
                    table.append_layout_element(Paragraph(""))

            # pop
            flowchart_methods = flowchart_methods[K:]

        # set some general properties
        table.set_padding_on_all_cells(
            padding_top=5, padding_right=5, padding_bottom=5, padding_left=5
        )

        layout: PageLayout = SingleColumnLayout(p)
        layout.append_layout_element(table)

        PDF.write(what=d, where_to="assets/test_all_flowchart_shapes.pdf")
