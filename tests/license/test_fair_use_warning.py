import io
import sys
import typing
from _decimal import Decimal
from pathlib import Path

from borb.license.usage_statistics import UsageStatistics
from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import Image
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import TableCell
from tests.test_case import TestCase


class TestFairUseWarning(TestCase):
    def test_fair_use_warning_10_per_minute(self):

        # set _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = 10

        # set sys.stdout
        prev_sys_stdout = sys.stdout
        new_sys_stdout = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
        sys.stdout = new_sys_stdout

        # write PDF documents
        for _ in range(0, 10):
            d: Document = Document()
            p: Page = Page()
            d.add_page(p)
            l: SingleColumnLayout = SingleColumnLayout(p)
            l.add(
                Paragraph(
                    "Lorem Ipsum", font_color=HexColor("56cbf9"), font_size=Decimal(20)
                )
            )
            l.add(Paragraph(Lipsum.generate_lipsum_text(5)))
            with open(self.get_first_output_file(), "wb") as fh:
                PDF.dumps(fh, d)

        # restore sys.stdout
        sys.stdout = prev_sys_stdout

        # restore _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )

        # check how many bytes were printed
        new_sys_stdout.seek(0)
        number_of_bytes_printed: int = len(str(new_sys_stdout.read()))
        assert number_of_bytes_printed >= 1024

    def test_fair_use_warning_50_per_minute(self):

        # set _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = 50

        # set sys.stdout
        prev_sys_stdout = sys.stdout
        new_sys_stdout = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
        sys.stdout = new_sys_stdout

        # write PDF documents
        for _ in range(0, 50):
            d: Document = Document()
            p: Page = Page()
            d.add_page(p)
            l: SingleColumnLayout = SingleColumnLayout(p)
            l.add(
                Paragraph(
                    "Lorem Ipsum", font_color=HexColor("56cbf9"), font_size=Decimal(20)
                )
            )
            l.add(Paragraph(Lipsum.generate_lipsum_text(5)))
            with open(self.get_second_output_file(), "wb") as fh:
                PDF.dumps(fh, d)

        # restore sys.stdout
        sys.stdout = prev_sys_stdout

        # restore _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )

        # check how many bytes were printed
        new_sys_stdout.seek(0)
        number_of_bytes_printed: int = len(str(new_sys_stdout.read()))
        assert number_of_bytes_printed >= 1024

    def test_fair_use_warning_100_per_minute(self):

        # set _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = 100

        # set sys.stdout
        prev_sys_stdout = sys.stdout
        new_sys_stdout = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
        sys.stdout = new_sys_stdout

        # write PDF documents
        for _ in range(0, 100):
            d: Document = Document()
            p: Page = Page()
            d.add_page(p)
            l: SingleColumnLayout = SingleColumnLayout(p)
            l.add(
                Paragraph(
                    "Lorem Ipsum", font_color=HexColor("56cbf9"), font_size=Decimal(20)
                )
            )
            l.add(Paragraph(Lipsum.generate_lipsum_text(5)))
            with open(self.get_third_output_file(), "wb") as fh:
                PDF.dumps(fh, d)

        # restore sys.stdout
        sys.stdout = prev_sys_stdout

        # restore _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )

        # check how many bytes were printed
        new_sys_stdout.seek(0)
        number_of_bytes_printed: int = len(str(new_sys_stdout.read()))
        assert number_of_bytes_printed >= 1024

    def _build_basic_invoice(self):

        d: Document = Document()

        p: Page = Page()
        d.add_page(p)

        l: SingleColumnLayout = SingleColumnLayout(p)

        l.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=5)
            .add(
                Image(
                    Path("/home/joris/Code/borb-dev/logo/borb_64.png"),
                    width=Decimal(100),
                    height=Decimal(100),
                )
            )
            .add(
                Paragraph(
                    "Invoice",
                    font_size=Decimal(30),
                    vertical_alignment=Alignment.MIDDLE,
                    horizontal_alignment=Alignment.RIGHT,
                )
            )
            .add(Paragraph("Billed To", font="Helvetica-Bold"))
            .add(Paragraph(""))
            .add(Paragraph("Imani Clowe"))
            .add(Paragraph("Invoice Nr 12345", horizontal_alignment=Alignment.RIGHT))
            .add(Paragraph("+123-456-7890"))
            .add(Paragraph("16 June 2023", horizontal_alignment=Alignment.RIGHT))
            .add(Paragraph("63 Ivy Road, Hawkville, GA, USA 31036"))
            .add(Paragraph(""))
            .no_borders()
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        l.add(
            FixedColumnWidthTable(
                number_of_columns=4, number_of_rows=7, padding_top=Decimal(30)
            )
            .add(
                TableCell(
                    Paragraph("Item", font="Helvetica-Bold"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Quantity", font="Helvetica-Bold"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Unit Price", font="Helvetica-Bold"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Total", font="Helvetica-Bold"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Eggshell Camisole Top"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(TableCell(Paragraph("1"), border_right=False, border_left=False))
            .add(TableCell(Paragraph("$123"), border_right=False, border_left=False))
            .add(TableCell(Paragraph("$123"), border_right=False, border_left=False))
            .add(
                TableCell(
                    Paragraph("Cuban Collar Shirt"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(TableCell(Paragraph("2"), border_right=False, border_left=False))
            .add(TableCell(Paragraph("$127"), border_right=False, border_left=False))
            .add(TableCell(Paragraph("$254"), border_right=False, border_left=False))
            .add(
                TableCell(
                    Paragraph("Floral Cotton Dress"),
                    border_right=False,
                    border_left=False,
                )
            )
            .add(TableCell(Paragraph("1"), border_right=False, border_left=False))
            .add(TableCell(Paragraph("$123"), border_right=False, border_left=False))
            .add(TableCell(Paragraph("$123"), border_right=False, border_left=False))
            .add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Subtotal", font="Helvetica-Bold"),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("$500"),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Tax (0%)", font="Helvetica-Bold"),
                    border_top=False,
                    border_right=False,
                    border_bottom=True,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("$0"),
                    border_top=False,
                    border_right=False,
                    border_bottom=True,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph(""),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("Total", font="Helvetica-Bold"),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .add(
                TableCell(
                    Paragraph("$500", font="Helvetica-Bold"),
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, d)

    def test_fair_use_warning_60_invoices_per_minute(self):

        # set _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = 60

        # set sys.stdout
        prev_sys_stdout = sys.stdout
        new_sys_stdout = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
        sys.stdout = new_sys_stdout

        # write PDF documents
        deltas: typing.List[int] = []
        for _ in range(0, 60):
            self._build_basic_invoice()

        # restore sys.stdout
        sys.stdout = prev_sys_stdout

        # restore _MAX_NUMBER_OF_DOCUMENTS_PER_MINUTE
        UsageStatistics._FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE = (
            prev_FAIR_USE_MAXIMUM_NUMBER_OF_DOCUMENTS_PER_MINUTE
        )

        # check how many bytes were printed
        new_sys_stdout.seek(0)
        number_of_bytes_printed: int = len(str(new_sys_stdout.read()))
        assert number_of_bytes_printed >= 1024
