import datetime
import random
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf import (
    Document,
    SingleColumnLayout,
    Paragraph,
    PageLayout,
    Page,
    FixedColumnWidthTable,
    HexColor,
    PDF,
    Lipsum,
)
from borb.pdf.canvas.layout.smart_art.smart_art import SmartArt
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddSmartArt(unittest.TestCase):
    """
    This test creates a PDF with a Paragraph object in it. The Paragraph is aligned TOP, LEFT.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_add_matrix(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(SmartArt.matrix(["lorem", "Ipsum", "Dolor", "Sit"]))

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_horizontal_bullet_list(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.horizontal_bullet_list(
                ["One", "Two", "Three"],
                [["Lorem", "Ipsum"], ["Dolor"], ["Sit", "Amet"]],
            )
        )

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_picture_list(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.picture_list(
                ["Lorem", "Ipsum", "Dolor"],
                [
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/512/Matryoshka-Leisure-icon.png",
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/128/Matryoshka-Music-icon.png",
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/128/Matryoshka-Pictures-icon.png",
                ],
            )
        )

        # determine output location
        out_file = self.output_dir / "output_003.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_alternating_picture_list(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.alternating_picture_list(
                ["Lorem", "Ipsum", "Dolor"],
                [
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/512/Matryoshka-Leisure-icon.png",
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/128/Matryoshka-Music-icon.png",
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/128/Matryoshka-Pictures-icon.png",
                ],
            )
        )

        # determine output location
        out_file = self.output_dir / "output_004.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_horizontal_process(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(SmartArt.horizontal_process(["Lorem", "Ipsum", "Dolor", "Amet"]))

        # determine output location
        out_file = self.output_dir / "output_005.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_vertical_process(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(SmartArt.vertical_process(["Lorem", "Ipsum", "Dolor", "Amet"]))

        # determine output location
        out_file = self.output_dir / "output_006.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_basic_bending_process_001(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.basic_bending_process(
                ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Consectetur", "Nunc"]
            )
        )

        # determine output location
        out_file = self.output_dir / "output_007.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_basic_bending_process_002(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.basic_bending_process(
                ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Consectetur"]
            )
        )

        # determine output location
        out_file = self.output_dir / "output_008.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_basic_bending_process_003(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.basic_bending_process(["Lorem", "Ipsum", "Dolor", "Sit", "Amet"])
        )

        # determine output location
        out_file = self.output_dir / "output_009.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_opposing_ideas(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(SmartArt.opposing_ideas(["Lorem Ipsum", "Dolor Sit Amet"]))

        # determine output location
        out_file = self.output_dir / "output_010.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_table_hierarchy(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        random.seed(2048)
        l.add(
            SmartArt.table_hierarcy(
                (
                    "Lorem",
                    [
                        ("Ipsum", [("Sit", [""]), ("Amet", [""])]),
                        ("Dolor", [("Consectetur", ["Consectetur", "Nunc", "Discet"])]),
                    ],
                )
            )
        )

        # determine output location
        out_file = self.output_dir / "output_011.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_vertical_bullet_list(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.vertical_bullet_list(
                ["One", "Two", "Three"],
                [["Lorem", "Ipsum"], ["Dolor"], ["Sit", "Amet"]],
            )
        )

        # determine output location
        out_file = self.output_dir / "output_012.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)

    def test_add_closed_chevron_process(self):
        d: Document = Document()
        p: Page = Page()
        d.add_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a SmartArt object in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        l.add(
            SmartArt.closed_chevron_process(
                ["One", "Two", "Three", "Four"],
            )
        )

        # determine output location
        out_file = self.output_dir / "output_013.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
