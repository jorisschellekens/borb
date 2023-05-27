from decimal import Decimal
from pathlib import Path

from borb.pdf import Table
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddParagraphsUsingTrueTypeFonts(TestCase):
    """
    This test loads a truetype _font from a .ttf file and attempts to use it to write 2 paragraphs of lorem ipsum.
    """

    def _write_document_with_font(
        self,
        font_name: str,
    ) -> Document:

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # layout
        layout: PageLayout = SingleColumnLayout(page)

        # add test information
        layout.add(
            self.get_test_header(
                f"This test loads {font_name} from a file and attempts to write letters and numbers with it."
            )
        )

        # path to _font
        font_path: Path = Path(__file__).parent / font_name
        assert font_path.exists()

        # load font
        ttf: TrueTypeFont = TrueTypeFont.true_type_font_from_file(font_path)

        # add paragraph 1
        uppercase_letter_table: Table = FixedColumnWidthTable(
            number_of_columns=5, number_of_rows=6
        )
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            try:
                uppercase_letter_table.add(Paragraph(c, font=ttf))
            except:
                uppercase_letter_table.add(Paragraph(""))
        uppercase_letter_table.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        layout.add(Paragraph("Uppercase:"))
        layout.add(uppercase_letter_table)

        # lowercase
        lowercase_letter_table: Table = FixedColumnWidthTable(
            number_of_columns=5, number_of_rows=6
        )
        for c in "abcdefghijklmnopqrstuvwxyz":
            try:
                lowercase_letter_table.add(Paragraph(c, font=ttf))
            except:
                lowercase_letter_table.add(Paragraph(""))
        lowercase_letter_table.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        layout.add(Paragraph("Lowercase:"))
        layout.add(lowercase_letter_table)

        # lowercase
        digit_table: Table = FixedColumnWidthTable(
            number_of_columns=5, number_of_rows=2
        )
        for c in "0123456789":
            try:
                digit_table.add(Paragraph(c, font=ttf))
            except:
                digit_table.add(Paragraph(""))
        digit_table.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        layout.add(Paragraph("Digits:"))
        layout.add(digit_table)

        # return
        return pdf

    def test_add_paragraphs_using_ubuntu_light(self):
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(
                in_file_handle, self._write_document_with_font("Ubuntu-Light.ttf")
            )
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_paragraphs_using_monaco_regular(self):
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(
                in_file_handle, self._write_document_with_font("Monaco-Regular.ttf")
            )
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_paragraphs_using_pacifico_regular(self):
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(
                in_file_handle, self._write_document_with_font("Pacifico-Regular.ttf")
            )
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_paragraphs_using_tourney(self):
        with open(self.get_fourth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, self._write_document_with_font("Tourney.ttf"))
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_paragraphs_using_simhei(self):
        with open(self.get_fifth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, self._write_document_with_font("SimHei.ttf"))
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
