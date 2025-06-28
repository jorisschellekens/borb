import unittest

from borb.pdf import (
    Document,
    Page,
    MultiColumnLayout,
    SmartArt,
    X11Color,
    PDF,
    Paragraph,
)


class TestSmartArtOverview(unittest.TestCase):

    def test_smart_art_overview(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: MultiColumnLayout = MultiColumnLayout(page=page, number_of_columns=3)

        # bending_process
        layout.append_layout_element(
            Paragraph(
                "Bending Process",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.bending_process(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=6,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # block_list
        layout.append_layout_element(
            Paragraph(
                "Block List", font_color=X11Color.PRUSSIAN_BLUE, font="Helvetica-Bold"
            )
        )
        layout.append_layout_element(
            SmartArt.block_list(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=6,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # circular_process
        layout.append_layout_element(
            Paragraph(
                "Circular Process",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.circular_process(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_ascending_list
        layout.append_layout_element(
            Paragraph(
                "Horizontal Ascending List",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_ascending_list(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=6,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_bullet_list
        layout.append_layout_element(
            Paragraph(
                "Horizontal Bullet List",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Lorem", "Ipsum"],
                level_2_items=[["Dolor", "Sit"], ["Amet", "Consectetur"]],
                level_1_font_size=6,
                level_2_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_descending_list
        layout.append_layout_element(
            Paragraph(
                "Horizontal Descending List",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_descending_list(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=6,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_equation
        layout.append_layout_element(
            Paragraph(
                "Horizontal Equation",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_equation(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_picture_list
        layout.append_layout_element(
            Paragraph(
                "Horizontal Picture List",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_picture_list(
                level_1_items=["Lorem", "Ipsum"],
                pictures=[
                    "https://images.unsplash.com/photo-1587883012610-e3df17d41270",
                    "https://images.unsplash.com/photo-1559181567-c3190ca9959b",
                ],
                picture_size=(16, 16),
                level_2_items=[["Dolor", "Sit"], ["Amet", "Consectetur"]],
                level_1_font_size=6,
                level_2_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_pie_process
        layout.append_layout_element(
            Paragraph(
                "Horizontal Pie Process",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_pie_process(
                level_1_items=["Lorem", "Ipsum"],
                level_2_items=[["Dolor", "Sit"], ["Amet", "Consectetur"]],
                level_1_font_size=6,
                level_2_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # horizontal_process
        layout.append_layout_element(
            Paragraph(
                "Horizontal Process",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.horizontal_process(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # inverted_pyramid
        layout.append_layout_element(
            Paragraph(
                "Inverted Pyramid",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.inverted_pyramid(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # opposing_ideas
        layout.append_layout_element(
            Paragraph(
                "Opposing Ideas",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.opposing_ideas(
                level_1_items=["Lorem", "Ipsum"],
                level_2_items=[["Dolor", "Sit"], ["Amet", "Consectetur"]],
                level_1_font_size=6,
                level_2_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # pyramid
        layout.append_layout_element(
            Paragraph(
                "Pyramid", font_color=X11Color.PRUSSIAN_BLUE, font="Helvetica-Bold"
            )
        )
        layout.append_layout_element(
            SmartArt.pyramid(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # tags
        layout.append_layout_element(
            Paragraph("Tags", font_color=X11Color.PRUSSIAN_BLUE, font="Helvetica-Bold")
        )
        layout.append_layout_element(
            SmartArt.tags(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # vertical_bullet_list
        layout.next_column()
        layout.append_layout_element(
            Paragraph(
                "Vertical Bullet List",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.vertical_bullet_list(
                level_1_items=["Lorem", "Ipsum"],
                level_2_items=[["Dolor", "Sit"], ["Amet", "Consectetur"]],
                level_1_font_size=6,
                level_2_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # vertical_equation
        layout.append_layout_element(
            Paragraph(
                "Vertical Equation",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.vertical_equation(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # vertical_picture_list
        layout.append_layout_element(
            Paragraph(
                "Vertical Picture List",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.vertical_picture_list(
                level_1_items=["Lorem", "Ipsum"],
                pictures=[
                    "https://images.unsplash.com/photo-1587883012610-e3df17d41270",
                    "https://images.unsplash.com/photo-1559181567-c3190ca9959b",
                ],
                picture_size=(16, 16),
                level_2_items=[["Dolor", "Sit"], ["Amet", "Consectetur"]],
                level_1_font_size=6,
                level_2_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # vertical_process
        layout.append_layout_element(
            Paragraph(
                "Vertical Process",
                font_color=X11Color.PRUSSIAN_BLUE,
                font="Helvetica-Bold",
            )
        )
        layout.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=["Lorem", "Ipsum", "Dolor", "Sit"],
                level_1_font_size=4,
                level_1_font_color=X11Color.WHITE,
                background_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        PDF.write(what=doc, where_to="assets/test_smart_art_overview.pdf")
