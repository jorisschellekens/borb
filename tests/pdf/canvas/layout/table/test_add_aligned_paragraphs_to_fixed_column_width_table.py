import typing

from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import Table
from borb.pdf import TableCell
from tests.test_case import TestCase


class TestAddAlignedParagraphsToFixedColumnWidthTable(TestCase):
    def test_add_fixed_column_width_table_001(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF. The FixedColumnWidthTable is filled with Paragraph objects."
            )
        )
        t: Table = FixedColumnWidthTable(number_of_columns=3, number_of_rows=3)
        ps: typing.List[Paragraph] = []
        for ha in [Alignment.RIGHT, Alignment.CENTERED, Alignment.LEFT]:
            for va in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]:
                ps += [
                    Paragraph(
                        f"{ha.name}, {va.name}",
                        horizontal_alignment=ha,
                        vertical_alignment=va,
                        background_color=HexColor("ff0000"),
                    )
                ]
                t.add(ps[-1])
        layout.add(t)
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_fixed_column_width_table_002(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF. The FixedColumnWidthTable is filled with Paragraph objects."
            )
        )

        for va in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]:
            t: Table = FixedColumnWidthTable(number_of_columns=2, number_of_rows=2)
            t.add(Paragraph("1"))
            t.add(
                TableCell(
                    Paragraph(
                        f"{va.name}",
                        vertical_alignment=va,
                        background_color=HexColor("ff0000"),
                    ),
                    row_span=2,
                )
            )
            t.add(Paragraph("2"))
            layout.add(t)

        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_fixed_column_width_table_003(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF. The FixedColumnWidthTable is filled with Paragraph objects."
            )
        )

        for va in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]:
            t: Table = FixedColumnWidthTable(number_of_columns=2, number_of_rows=3)
            t.add(Paragraph("1"))
            t.add(
                TableCell(
                    Paragraph(
                        f"{va.name}",
                        vertical_alignment=va,
                        background_color=HexColor("ff0000"),
                    ),
                    row_span=3,
                )
            )
            t.add(Paragraph("2"))
            t.add(Paragraph("3"))
            layout.add(t)

        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_fixed_column_width_table_004(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF. The FixedColumnWidthTable is filled with Paragraph objects."
            )
        )

        for va in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]:
            t: Table = FixedColumnWidthTable(number_of_columns=3, number_of_rows=3)
            t.add(Paragraph("1"))
            t.add(
                TableCell(
                    Paragraph(
                        f"{va.name}",
                        vertical_alignment=va,
                        background_color=HexColor("ff0000"),
                    ),
                    row_span=3,
                )
            )
            t.add(Paragraph("2"))
            t.add(Paragraph("3"))
            t.add(Paragraph("4"))
            t.add(Paragraph("5"))
            t.add(Paragraph("6"))
            layout.add(t)

        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_fixed_column_width_table_005(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF. The FixedColumnWidthTable is filled with Paragraph objects."
            )
        )

        for va in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]:
            t: Table = FixedColumnWidthTable(number_of_columns=4, number_of_rows=3)
            t.add(
                TableCell(
                    Paragraph(
                        f"{va.name}",
                        vertical_alignment=va,
                        background_color=HexColor("ff0000"),
                    ),
                    row_span=3,
                )
            )
            t.add(Paragraph("1"))
            t.add(
                TableCell(
                    Paragraph(
                        f"{va.name}",
                        vertical_alignment=va,
                        background_color=HexColor("ff0000"),
                    ),
                    row_span=3,
                )
            )
            t.add(Paragraph("2"))
            t.add(Paragraph("3"))
            t.add(Paragraph("4"))
            t.add(Paragraph("5"))
            t.add(Paragraph("6"))
            layout.add(t)

        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())
