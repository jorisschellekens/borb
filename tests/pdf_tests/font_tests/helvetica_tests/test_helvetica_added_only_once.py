import unittest

from borb.pdf import (
    Document,
    Page,
    Standard14Fonts,
    Font,
    SingleColumnLayout,
    PageLayout,
    Paragraph,
    PDF,
    FlexibleColumnWidthTable,
    Table,
    LineArt,
    HSVColor,
)


class TestHelveticaAddedOnlyOnce(unittest.TestCase):

    def test_helvetica_added_only_once(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        font: Font = Standard14Fonts.get("Helvetica")

        # add Paragraph(s)
        layout: PageLayout = SingleColumnLayout(p)

        t: Table = FlexibleColumnWidthTable(number_of_columns=5, number_of_rows=5 * 2)
        for i in range(0, 5):
            for j in range(0, 5):
                t.append_layout_element(
                    LineArt.square(
                        fill_color=HSVColor(hue=i / 4, saturation=j / 4, value=j / 4),
                        stroke_color=HSVColor(hue=i / 4, saturation=j / 4, value=j / 4),
                    ).scale_to_fit(size=(30, 30))
                )
            for j in range(0, 5):
                t.append_layout_element(
                    Paragraph(f"{round(i/4, 2)}{round(j/4, 2)} {round(j/4, 2)}")
                )

        t.set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        )
        layout.append_layout_element(t)

        # store
        PDF.write(what=d, where_to="assets/test_helvetica_added_only_once.pdf")
