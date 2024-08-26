from decimal import Decimal

from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import GoogleTrueTypeFont
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import Table
from borb.pdf import TrueTypeFont
from tests.test_case import TestCase


class TestAddParagraphsUsingGoogleFonts(TestCase):
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

        # load font
        ttf: TrueTypeFont = GoogleTrueTypeFont.true_type_font_from_google(font_name)

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

    def test_add_paragraphs_using_jacquard_12(self):

        # set GOOGLE_FONTS_API_KEY
        try:
            from tests.secrets import populate_os_environ

            populate_os_environ()
        except:
            pass

        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, self._write_document_with_font("Jacquard 12"))
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_paragraphs_using_pacifico(self):

        # set GOOGLE_FONTS_API_KEY
        try:
            from tests.secrets import populate_os_environ

            populate_os_environ()
        except:
            pass

        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, self._write_document_with_font("Pacifico"))
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_paragraphs_using_shadows_into_light(self):

        # set GOOGLE_FONTS_API_KEY
        try:
            from tests.secrets import populate_os_environ

            populate_os_environ()
        except:
            pass

        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(
                in_file_handle, self._write_document_with_font("Shadows Into Light")
            )
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())
