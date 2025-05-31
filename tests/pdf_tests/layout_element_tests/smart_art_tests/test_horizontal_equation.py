import unittest

from borb.pdf import PDF, SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestHorizontalEquation(unittest.TestCase):

    def test_horizontal_equation_3_items(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                ],
            )
        )

        PDF.write(what=d, where_to="assets/test_horizontal_equation_3_items.pdf")

    def test_horizontal_equation_4_items(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                ],
            )
        )

        PDF.write(what=d, where_to="assets/test_horizontal_equation_4_items.pdf")
