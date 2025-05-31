import random
import unittest

from borb.pdf import (
    Page,
    Document,
    PageLayout,
    SingleColumnLayout,
    FlexibleColumnWidthTable,
    Table,
    Lipsum,
    Barcode,
    Emoji,
    LineArt,
    PDF,
    Paragraph,
    UnorderedList,
    OrderedList,
    RomanNumeralOrderedList,
    ABCOrderedList,
    ProgressSquare,
    X11Color,
    Standard14Fonts,
)


class TestSmoke(unittest.TestCase):

    def test_smoke(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        t: Table = FlexibleColumnWidthTable(number_of_columns=4, number_of_rows=8)

        # emoji
        t.append_layout_element(Emoji.AERIAL_TRAMWAY)
        t.append_layout_element(Emoji.BABY)
        t.append_layout_element(Emoji.CACTUS)
        t.append_layout_element(Emoji.DANCER)

        # barcode
        t.append_layout_element(
            Barcode(
                barcode_data="01234567890",
                barcode_type=Barcode.BarcodeType.CODE_128,
                size=(64, 64),
            )
        )
        t.append_layout_element(
            Barcode(
                barcode_data="01234567890",
                barcode_type=Barcode.BarcodeType.CODE_39,
                size=(64, 64),
            )
        )
        t.append_layout_element(
            Barcode(
                barcode_data="01234567890",
                barcode_type=Barcode.BarcodeType.EAN_8,
                size=(64, 64),
            )
        )
        t.append_layout_element(
            Barcode(
                barcode_data="012345678900",
                barcode_type=Barcode.BarcodeType.EAN_13,
                size=(64, 64),
            )
        )

        # line art
        t.append_layout_element(
            LineArt.fraction_of_circle(angle_in_degrees=30).scale_to_fit(size=(64, 64))
        )
        t.append_layout_element(
            LineArt.fraction_of_circle(angle_in_degrees=60).scale_to_fit(size=(64, 64))
        )
        t.append_layout_element(
            LineArt.fraction_of_circle(angle_in_degrees=90).scale_to_fit(size=(64, 64))
        )
        t.append_layout_element(
            LineArt.fraction_of_circle(angle_in_degrees=120).scale_to_fit(size=(64, 64))
        )

        # line art
        random.seed(0)
        t.append_layout_element(
            LineArt.blob(stroke_color=X11Color.PRUSSIAN_BLUE).scale_to_fit(
                size=(64, 64)
            )
        )
        t.append_layout_element(
            LineArt.blob(stroke_color=X11Color.PRUSSIAN_BLUE).scale_to_fit(
                size=(64, 64)
            )
        )
        t.append_layout_element(
            LineArt.blob(stroke_color=X11Color.PRUSSIAN_BLUE).scale_to_fit(
                size=(64, 64)
            )
        )
        t.append_layout_element(
            LineArt.blob(stroke_color=X11Color.PRUSSIAN_BLUE).scale_to_fit(
                size=(64, 64)
            )
        )

        # line art
        t.append_layout_element(
            LineArt.dragon_curve(number_of_iterations=5).scale_to_fit(size=(64, 64))
        )
        t.append_layout_element(
            LineArt.dragon_curve(number_of_iterations=6).scale_to_fit(size=(64, 64))
        )
        t.append_layout_element(
            LineArt.dragon_curve(number_of_iterations=7).scale_to_fit(size=(64, 64))
        )
        t.append_layout_element(
            LineArt.dragon_curve(number_of_iterations=8).scale_to_fit(size=(64, 64))
        )

        # text
        t.append_layout_element(
            Paragraph(Lipsum.generate_lorem_ipsum(64), font_size=12)
        )
        t.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(64),
                font_size=12,
                font=Standard14Fonts.get("Helvetica-Bold"),
            )
        )
        t.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(64),
                font_size=12,
                font=Standard14Fonts.get("Helvetica-Italic"),
            )
        )
        t.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(64),
                font_size=12,
                font=Standard14Fonts.get("Helvetica-Bold-Italic"),
            )
        )

        # lists
        t.append_layout_element(
            UnorderedList()
            .append_layout_element(Paragraph("Lorem"))
            .append_layout_element(Paragraph("Ipsum"))
            .append_layout_element(Paragraph("Dolor"))
        )
        t.append_layout_element(
            OrderedList()
            .append_layout_element(Paragraph("Sit"))
            .append_layout_element(Paragraph("Amet"))
            .append_layout_element(Paragraph("Consectetur"))
        )
        t.append_layout_element(
            ABCOrderedList()
            .append_layout_element(Paragraph("Lorem"))
            .append_layout_element(Paragraph("Ipsum"))
            .append_layout_element(Paragraph("Dolor"))
        )
        t.append_layout_element(
            RomanNumeralOrderedList()
            .append_layout_element(Paragraph("Sit"))
            .append_layout_element(Paragraph("Amet"))
            .append_layout_element(Paragraph("Consectetur"))
        )

        # progress bar
        t.append_layout_element(ProgressSquare(value=20, width=32))
        t.append_layout_element(ProgressSquare(value=40, width=32))
        t.append_layout_element(ProgressSquare(value=60, width=32))
        t.append_layout_element(ProgressSquare(value=80, width=32))

        #
        t.set_padding_on_all_cells(
            padding_top=5, padding_right=5, padding_bottom=5, padding_left=5
        )
        l.append_layout_element(t)

        PDF.write(what=d, where_to="assets/test_smoke.pdf")
