import unittest

from borb.pdf import PDF, SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestHorizontalDescendingList(unittest.TestCase):

    def test_horizontal_descending_list(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_descending_list(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                    "Manganese",
                    "Vitamin D",
                ],
            )
        )

        PDF.write(what=d, where_to="assets/test_horizontal_descending_list.pdf")
