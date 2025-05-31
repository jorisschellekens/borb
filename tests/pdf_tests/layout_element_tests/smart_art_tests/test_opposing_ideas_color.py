import unittest

from borb.pdf import PDF, SmartArt, X11Color
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestOpposingIdeasColor(unittest.TestCase):

    def test_opposing_ideas_color_red(self):
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
                background_color=X11Color.RED,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_red.pdf")

    def test_opposing_ideas_color_orange(self):
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
                background_color=X11Color.ORANGE,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_orange.pdf")

    def test_opposing_ideas_color_yellow(self):
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
                background_color=X11Color.YELLOW_MUNSELL,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_yellow.pdf")

    def test_opposing_ideas_color_green(self):
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
                background_color=X11Color.GREEN_YELLOW,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_green.pdf")

    def test_opposing_ideas_color_blue(self):
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
                background_color=X11Color.BLUE,
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_blue.pdf")

    def test_opposing_ideas_color_indigo(self):
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
                background_color=X11Color.INDIGO,
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_indigo.pdf")

    def test_opposing_ideas_color_violet(self):
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
                background_color=X11Color.VIOLET,
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_opposing_ideas_color_violet.pdf")
