from _decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import Image
from borb.pdf import OrderedList
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import TableCell
from borb.pdf import UnorderedList
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from tests.test_case import TestCase


class TestAddFixedColumnWidthTable(TestCase):
    def test_add_fixed_column_width_table_2_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_fixed_column_width_table_3_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=3, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
            .add(Paragraph("Adipiscing"))
            .add(Paragraph("Elit Sed"))
            .add(Paragraph("Do Eiusmod"))
        )
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_fixed_column_width_table_3_by_4(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=3, number_of_rows=4)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
            .add(Paragraph("Adipiscing"))
            .add(Paragraph("Elit Sed"))
            .add(Paragraph("Do Eiusmod"))
            .add(Paragraph("Tempor Incididunt Ut"))
            .add(Paragraph("Labore et Dolore"))
            .add(Paragraph("Magna Aliqua"))
        )
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_fixed_column_width_table_incomplete_2_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
        )
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_fixed_column_width_table_using_horizontal_alignment_left(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using horizontal alignment LEFT"
            )
        )
        layout.add(
            FixedColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                horizontal_alignment=Alignment.LEFT,
            )
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
        )
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_fixed_column_width_table_using_horizontal_alignment_centered(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using horizontal alignment CENTERED."
            )
        )
        layout.add(
            FixedColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                horizontal_alignment=Alignment.CENTERED,
            )
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
        )
        with open(self.get_sixth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_fixed_column_width_table_using_horizontal_alignment_right(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF  using horizontal alignment RIGHT."
            )
        )
        layout.add(
            FixedColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                horizontal_alignment=Alignment.RIGHT,
            )
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
        )
        with open(self.get_seventh_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_fixed_column_width_table_no_borders(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF without borders."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
            .no_borders()
        )
        with open(self.get_eight_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_add_fixed_column_width_table_internal_borders(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with internal borders."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
            .no_borders()
            .internal_borders()
        )
        with open(self.get_nineth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())

    def test_add_fixed_column_width_table_rounded_corners(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with rounded borders."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(TableCell(Paragraph("Lorem"), border_radius_top_left=Decimal(10)))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
        )
        with open(self.get_tenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_tenth_output_file())
        self.check_pdf_using_validator(self.get_tenth_output_file())

    def test_add_fixed_column_width_table_padding_on_all_cells(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with padding on all cells."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )
        with open(self.get_eleventh_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_eleventh_output_file())
        self.check_pdf_using_validator(self.get_eleventh_output_file())

    def test_add_fixed_column_width_table_even_odd_row_colors(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with even/odd row colors."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
            .add(Paragraph("Consectetur"))
            .even_odd_row_colors(
                even_row_color=HexColor("ffffff"), odd_row_color=HexColor("efefef")
            )
        )
        with open(self.get_twelfth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_twelfth_output_file())
        self.check_pdf_using_validator(self.get_twelfth_output_file())

    def test_add_fixed_column_width_table_row_span(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with row_span."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(TableCell(Paragraph("Lorem"), row_span=2))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
        )
        with open(self.get_thirteenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_thirteenth_output_file())
        self.check_pdf_using_validator(self.get_thirteenth_output_file())

    def test_add_fixed_column_width_table_col_span(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with col_span."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(TableCell(Paragraph("Lorem"), column_span=2))
            .add(Paragraph("Ipsum"))
            .add(Paragraph("Dolor"))
            .add(Paragraph("Sit"))
            .add(Paragraph("Amet"))
        )
        with open(self.get_fourteenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fourteenth_output_file())
        self.check_pdf_using_validator(self.get_fourteenth_output_file())

    def test_add_fixed_column_width_table_mixed_content(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF with mixed content."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Lorem"))
            .add(
                OrderedList()
                .add(Paragraph("Ipsum"))
                .add(Paragraph("Dolor"))
                .add(Paragraph("Sit"))
            )
            .add(
                UnorderedList()
                .add(Paragraph("Consectetur"))
                .add(Paragraph("Adipiscing"))
                .add(Paragraph("Elit"))
            )
            .add(Emojis.BIRD.value)
            .add(Emojis.OCTOCAT.value)
            .add(
                Image(
                    "https://images.unsplash.com/photo-1515092557918-3885fa25718f",
                    width=Decimal(64),
                    height=Decimal(64),
                )
            )
        )
        with open(self.get_fifteenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fifteenth_output_file())
        self.check_pdf_using_validator(self.get_fifteenth_output_file())
