import unittest

from borb.pdf import PDF, SmartArt, PageSize
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestHorizontalPictureList(unittest.TestCase):

    def test_horizontal_picture_list(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_picture_list(
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
            )
        )

        PDF.write(what=d, where_to="assets/test_horizontal_picture_list.pdf")
