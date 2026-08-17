from borb.pdf import SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from tests.test_case import TestCase


class TestVerticalEquationFontSize(TestCase):

    def test_vertical_equation_font_size_small(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                ],
                level_1_font_size=8,
            )
        )

        TestCase.write(what=d, where_to="test_vertical_equation_font_size_small.pdf")

    def test_vertical_equation_font_size_regular(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                ],
                level_1_font_size=12,
            )
        )

        TestCase.write(what=d, where_to="test_vertical_equation_font_size_regular.pdf")

    def test_vertical_equation_font_size_large(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                ],
                level_1_font_size=16,
            )
        )

        TestCase.write(what=d, where_to="test_vertical_equation_font_size_large.pdf")
