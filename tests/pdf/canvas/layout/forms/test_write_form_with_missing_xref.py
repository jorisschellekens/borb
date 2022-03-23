import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.forms.push_button import PushButton, JavaScriptPushButton
from borb.pdf.canvas.layout.forms.text_area import TextArea
from borb.pdf.canvas.layout.forms.text_field import TextField
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
    FixedColumnWidthTable,
)
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWriteFormWithMissingXRef(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
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

    def test_write_form_using_flexiblecolumnwidthtable(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    """
            This test creates a PDF with a form in it. 
            Because of the way forms are initialized, they need an XREF to be present at layout.
            This, combined with FlexibleColumnWidthTable was a problem previously, causing a KeyError. This should be fixed.
                           """
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add empty space
        layout.add(Paragraph(" "))

        # add form
        layout.add(
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=9)
            .add(Paragraph("User Name: "))
            .add(TextField(field_name="username"))
            .add(Paragraph("ID: "))
            .add(TextField(field_name="eid"))
            .add(Paragraph("Computer Name: "))
            .add(TextField(field_name="newpcname"))
            .add(Paragraph("Replacing Computer: "))
            .add(TextField(field_name="oldpcname"))
            .add(Paragraph("S/N: "))
            .add(TextField(field_name="oldserial"))
            .add(Paragraph("Keep in Service"))
            .add(TextField(field_name="service"))
            .add(Paragraph("Location"))
            .add(TextField(field_name="location"))
            .add(Paragraph("Model: "))
            .add(TextField(field_name="model"))
            .add(Paragraph("S/N: "))
            .add(TextField(field_name="serial"))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            .no_borders()
        )

        # write
        file = self.output_dir / "output_001.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)


if __name__ == "__main__":
    unittest.main()
