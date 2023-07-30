import random
from _decimal import Decimal

from borb.pdf import Document
from borb.pdf import Lipsum
from borb.pdf import MultiColumnLayout
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import ThreeColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import TwoColumnLayout
from borb.pdf.page.page_size import PageSize
from tests.test_case import TestCase


class TestMultiColumnLayout(TestCase):
    def test_multicolumnlayout_with_1_column(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 1 column"
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))
        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    #
    # 2
    #

    def test_multicolumnlayout_with_2_columns(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = TwoColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 2 columns",
                font_size=Decimal(8),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))
        with open(self.get_second_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_multicolumnlayout_with_2_columns_inter_column_margin_10(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        layout = MultiColumnLayout(
            page,
            column_widths=[
                w * Decimal(0.70) * Decimal(0.5),
                w * Decimal(0.70) * Decimal(0.5),
            ],
            margin_top=h * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            inter_column_margins=[w * Decimal(0.1)],
        )
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 2 columns.",
                font_size=Decimal(8),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))
        with open(self.get_third_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_multicolumnlayout_with_2_columns_inter_column_margin_15(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        layout = MultiColumnLayout(
            page,
            column_widths=[
                w * Decimal(0.65) * Decimal(0.5),
                w * Decimal(0.65) * Decimal(0.5),
            ],
            margin_top=h * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            inter_column_margins=[w * Decimal(0.15)],
        )
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 2 columns.",
                font_size=Decimal(8),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))
        with open(self.get_fourth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_multicolumnlayout_with_2_columns_inter_column_margin_20(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        layout = MultiColumnLayout(
            page,
            column_widths=[
                w * Decimal(0.60) * Decimal(0.5),
                w * Decimal(0.60) * Decimal(0.5),
            ],
            margin_top=h * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            inter_column_margins=[w * Decimal(0.20)],
        )
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 2 columns.",
                font_size=Decimal(8),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s))
        with open(self.get_fifth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    #
    # 3
    #

    def test_multicolumnlayout_with_3_columns(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        layout = ThreeColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 3 columns",
                font_size=Decimal(4),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s, font_size=Decimal(8)))
        with open(self.get_sixth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_multicolumnlayout_with_3_columns_inter_column_margin_10(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        layout = MultiColumnLayout(
            page,
            column_widths=[
                w * Decimal(0.60) / Decimal(3),
                w * Decimal(0.60) / Decimal(3),
                w * Decimal(0.60) / Decimal(3),
            ],
            margin_top=h * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            inter_column_margins=[w * Decimal(0.10), w * Decimal(0.10)],
        )
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 3 columns.",
                font_size=Decimal(4),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s, font_size=Decimal(8)))
        with open(self.get_seventh_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_multicolumnlayout_with_3_columns_inter_column_margin_15(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        layout = MultiColumnLayout(
            page,
            column_widths=[
                w * Decimal(0.50) / Decimal(3),
                w * Decimal(0.50) / Decimal(3),
                w * Decimal(0.50) / Decimal(3),
            ],
            margin_top=h * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            inter_column_margins=[w * Decimal(0.15), w * Decimal(0.15)],
        )
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 3 columns.",
                font_size=Decimal(4),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s, font_size=Decimal(8)))
        with open(self.get_eight_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_multicolumnlayout_with_3_columns_inter_column_margin_20(self):
        pdf = Document()
        page = Page()
        pdf.add_page(page)
        w = page.get_page_info().get_width()
        h = page.get_page_info().get_height()
        layout = MultiColumnLayout(
            page,
            column_widths=[
                w * Decimal(0.40) / Decimal(3),
                w * Decimal(0.40) / Decimal(3),
                w * Decimal(0.40) / Decimal(3),
            ],
            margin_top=h * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            inter_column_margins=[w * Decimal(0.20), w * Decimal(0.20)],
        )
        layout.add(
            self.get_test_header(
                test_description="This test sets a MultiColumnLayout to a PDF with 3 columns.",
                font_size=Decimal(3),
            )
        )
        random.seed(0)
        for s in [
            Lipsum.generate_arthur_conan_doyle_text(random.choice([5, 6, 7]))
            for _ in range(0, 5)
        ]:
            layout.add(Paragraph(s, font_size=Decimal(8)))
        with open(self.get_nineth_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())
