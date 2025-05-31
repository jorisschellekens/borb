import unittest

from borb.pdf import PDF, SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestOpposingIdeasFontSize(unittest.TestCase):

    def test_opposing_ideas_font_size_small(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.opposing_ideas(
                level_1_items=["Cherries", "Papaya"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                ],
                level_1_font_size=8,
                level_2_font_size=6,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_font_size_small.pdf")

    def test_opposing_ideas_font_size_regular(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.opposing_ideas(
                level_1_items=["Cherries", "Papaya"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                ],
                level_1_font_size=12,
                level_2_font_size=10,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_font_size_regular.pdf")

    def test_opposing_ideas_font_size_large(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.opposing_ideas(
                level_1_items=["Cherries", "Papaya"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                ],
                level_1_font_size=16,
                level_2_font_size=14,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_font_size_large.pdf")
