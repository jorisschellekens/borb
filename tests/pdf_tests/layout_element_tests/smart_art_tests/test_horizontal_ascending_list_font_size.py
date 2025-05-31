import unittest

from borb.pdf import PDF, SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestHorizontalAscendingListFontSize(unittest.TestCase):

    def test_horizontal_ascending_list_font_size_small(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_ascending_list(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                    "Manganese",
                    "Vitamin D",
                ],
                level_1_font_size=8,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_font_size_small.pdf"
        )

    def test_horizontal_ascending_list_font_size_regular(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_ascending_list(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                    "Manganese",
                    "Vitamin D",
                ],
                level_1_font_size=12,
            )
        )

        PDF.write(
            what=d,
            where_to="assets/test_horizontal_ascending_list_font_size_regular.pdf",
        )

    def test_horizontal_ascending_list_font_size_large(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_ascending_list(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                    "Manganese",
                    "Vitamin D",
                ],
                level_1_font_size=16,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_font_size_large.pdf"
        )
