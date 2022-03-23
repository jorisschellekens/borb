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
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestWritePushButton(unittest.TestCase):
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

    def test_write_push_button_at_absolute_position(self):

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
            .add(Paragraph("This test creates a PDF with a PushButton in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write TextField
        tf: PushButton = PushButton("Click Me!")
        tf.layout(
            page, Rectangle(Decimal(59), Decimal(600), Decimal(476), Decimal(12.5 * 5))
        )

        # write
        file = self.output_dir / "output_001.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_write_push_button_using_layout_manager(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # layout manager
        l: PageLayout = SingleColumnLayout(page)

        # write test info
        l.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with a few TextField objects and a TextArea in it."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write TextField
        l.add(
            FixedColumnWidthTable(
                number_of_rows=4, number_of_columns=2, margin_top=Decimal(20)
            )
            .add(Paragraph("Name:"))
            .add(
                TextField(
                    value="Doe", font_color=HexColor("56cbf9"), font_size=Decimal(20)
                )
            )
            .add(Paragraph("Firstname:"))
            .add(
                TextField(
                    value="John", font_color=HexColor("56cbf9"), font_size=Decimal(20)
                )
            )
            .add(Paragraph("Place of residence:"))
            .add(TextArea(field_name="place_of_residence"))
            .add(Paragraph(" "))
            .add(PushButton("Submit!", horizontal_alignment=Alignment.RIGHT))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write
        file = self.output_dir / "output_002.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_check_acroform_present(self):

        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_002.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        assert doc is not None
        assert doc.get_page(0).has_acroforms()

    def test_write_javascript_push_button_using_layout_manager(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # layout manager
        l: PageLayout = SingleColumnLayout(page)

        # write test info
        l.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph("This test creates a PDF with a JavaScript PushButton in it.")
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add JavaSciptPushButton
        l.add(
            JavaScriptPushButton(
                text="Hello World!",
                javascript="app.alert('Hello World', 3)",
                horizontal_alignment=Alignment.RIGHT,
                margin_top=Decimal(10),
            )
        )

        # write
        file = self.output_dir / "output_003.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)


if __name__ == "__main__":
    unittest.main()
