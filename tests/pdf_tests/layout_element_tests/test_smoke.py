import pathlib
import random
import typing
from unittest import TestCase

from borb.pdf import (
    Page,
    Document,
    PageLayout,
    SingleColumnLayout,
    FlexibleColumnWidthTable,
    Table,
    Lipsum,
    LineArt,
    Paragraph,
    UnorderedList,
    OrderedList,
    RomanNumeralOrderedList,
    ABCOrderedList,
    ProgressSquare,
    X11Color,
    Standard14Fonts,
    PDF,
)


class TestSmoke(TestCase):

    # Note: This class does not inherit from the borb TestCase
    #       because we execute it as a smoke test, and do not want to drag in
    #       unneeded dependencies (PIL) for doing a visual comparison.

    #
    # PRIVATE
    #

    @staticmethod
    def __get_assets_dir() -> pathlib.Path:
        return TestSmoke.__get_project_dir() / "tests" / "assets"

    @staticmethod
    def __get_project_dir() -> pathlib.Path:
        me: pathlib.Path = pathlib.Path(__file__).resolve().parent
        while True:
            if (me / ".git").is_dir():
                return me
            if me.parent == me:
                break  # reached filesystem root
            me = me.parent
        raise FileNotFoundError(
            "Could not find project root (.git directory not found)"
        )

    @staticmethod
    def __write(
        what: Document,
        where_to: typing.Union[pathlib.Path, str, typing.BinaryIO],
    ) -> None:

        # canonize
        if isinstance(where_to, str):
            where_to = pathlib.Path(where_to)
        where_to = TestSmoke.__get_assets_dir() / where_to.name

        # write
        PDF.write(what=what, where_to=where_to)

        # IF we are writing to a stream
        # THEN we can't really compare to the ground truth
        if isinstance(where_to, typing.BinaryIO):
            return

        # determine the ground-truth name
        stem: typing.Optional[str] = None
        if isinstance(where_to, pathlib.Path):
            stem = where_to.stem
        if isinstance(where_to, str):
            stem = pathlib.Path(where_to).stem
        assert stem is not None

    #
    # PUBLIC
    #

    def test_smoke(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        t: Table = FlexibleColumnWidthTable(number_of_columns=4, number_of_rows=6)

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

        TestSmoke.__write(what=d, where_to="test_smoke.pdf")
