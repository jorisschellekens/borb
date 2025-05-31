import unittest

from borb.pdf import PDF, SmartArt, X11Color, PageSize
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TestVerticalProcessColor(unittest.TestCase):

    def test_vertical_process_color_red(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.RED,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_red.pdf")

    def test_vertical_process_color_orange(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.ORANGE,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_orange.pdf")

    def test_vertical_process_color_yellow(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.YELLOW_MUNSELL,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_yellow.pdf")

    def test_vertical_process_color_green(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.GREEN_YELLOW,
                level_1_font_color=X11Color.BLACK,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_green.pdf")

    def test_vertical_process_color_blue(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.BLUE,
                level_1_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_white.pdf")

    def test_vertical_process_color_indigo(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.INDIGO,
                level_1_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_indigo.pdf")

    def test_vertical_process_color_violet(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                    "Fiber",
                ],
                background_color=X11Color.VIOLET,
                level_1_font_color=X11Color.WHITE,
            )
        )

        PDF.write(what=d, where_to="assets/test_vertical_process_color_violet.pdf")
