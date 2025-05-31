import unittest

from borb.pdf import PDF, SmartArt, X11Color
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestVerticalPictureListColor(unittest.TestCase):

    def test_vertical_picture_list_color_red(self):
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
                background_color=X11Color.RED,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DIM_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_red.pdf")

    def test_vertical_picture_list_color_orange(self):
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
                background_color=X11Color.ORANGE,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DIM_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_orange.pdf")

    def test_vertical_picture_list_color_yellow(self):
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
                background_color=X11Color.YELLOW_MUNSELL,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DIM_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_yellow.pdf")

    def test_vertical_picture_list_color_green(self):
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
                background_color=X11Color.GREEN_YELLOW,
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DIM_GRAY,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_green.pdf")

    def test_vertical_picture_list_color_blue(self):
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
                background_color=X11Color.BLUE,
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_blue.pdf")

    def test_vertical_picture_list_color_indigo(self):
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
                background_color=X11Color.INDIGO,
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_indigo.pdf")

    def test_vertical_picture_list_color_violet(self):
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
                background_color=X11Color.VIOLET,
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_picture_list_color_violet.pdf")
