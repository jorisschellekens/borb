import unittest

from borb.pdf import PDF, SmartArt, X11Color
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestHorizontalAscendingListColor(unittest.TestCase):

    def test_horizontal_ascending_list_color_red(self):
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
                background_color=X11Color.RED,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_red.pdf"
        )

    def test_horizontal_ascending_list_color_orange(self):
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
                background_color=X11Color.ORANGE,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_orange.pdf"
        )

    def test_horizontal_ascending_list_color_yellow(self):
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
                background_color=X11Color.YELLOW_MUNSELL,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_yellow.pdf"
        )

    def test_horizontal_ascending_list_color_green(self):
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
                background_color=X11Color.GREEN_YELLOW,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_green.pdf"
        )

    def test_horizontal_ascending_list_color_blue(self):
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
                background_color=X11Color.BLUE,
                level_1_font_color=X11Color.WHITE,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_blue.pdf"
        )

    def test_horizontal_ascending_list_color_indigo(self):
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
                background_color=X11Color.INDIGO,
                level_1_font_color=X11Color.WHITE,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_indigo.pdf"
        )

    def test_horizontal_ascending_list_color_violet(self):
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
                background_color=X11Color.VIOLET,
                level_1_font_color=X11Color.WHITE,
            )
        )

        PDF.write(
            what=d, where_to="assets/test_horizontal_ascending_list_color_violet.pdf"
        )
