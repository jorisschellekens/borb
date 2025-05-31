import unittest

from borb.pdf import PDF, SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestVerticalPictureListFontSize(unittest.TestCase):

    def test_vertical_picture_list_font_size_small(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_picture_list(
                pictures=[
                    "https://images.unsplash.com/photo-1559181567-c3190ca9959b",
                    "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe",
                    "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578",
                ],
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                picture_size=(64, 64),
                level_1_font_size=8,
                level_2_font_size=6,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_vertical_picture_list_font_size_small.pdf"
        )

    def test_vertical_picture_list_font_size_regular(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_picture_list(
                pictures=[
                    "https://images.unsplash.com/photo-1559181567-c3190ca9959b",
                    "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe",
                    "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578",
                ],
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                picture_size=(64, 64),
                level_1_font_size=12,
                level_2_font_size=10,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_vertical_picture_list_font_size_regular.pdf"
        )

    def test_vertical_picture_list_font_size_large(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_picture_list(
                pictures=[
                    "https://images.unsplash.com/photo-1559181567-c3190ca9959b",
                    "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe",
                    "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578",
                ],
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                picture_size=(64, 64),
                level_1_font_size=16,
                level_2_font_size=14,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_vertical_picture_list_font_size_large.pdf"
        )
