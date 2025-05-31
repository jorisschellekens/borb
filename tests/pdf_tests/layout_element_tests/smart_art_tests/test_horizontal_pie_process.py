import unittest

from borb.pdf import PDF, SmartArt, PageSize
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestHorizontalPieProcess(unittest.TestCase):

    def test_horizontal_pie_process(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_pie_process(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
            )
        )

        PDF.write(what=d, where_to="assets/test_horizontal_pie_process.pdf")
