import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.forms.country_drop_down_list import CountryDropDownList
from borb.pdf.canvas.layout.forms.drop_down_list import DropDownList
from borb.pdf.canvas.layout.forms.text_field import TextField
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteDropDownList(unittest.TestCase):
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

    def test_write_drop_down_list_at_absolute_position(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # write TextField
        tf: DropDownList = DropDownList(
            possible_values=[
                "Afghanistan",
                "Albania",
                "Algeria",
                "Andorra",
            ]
        )
        tf.layout(
            page, Rectangle(Decimal(105), Decimal(764), Decimal(419), Decimal(15))
        )

        # write
        file = self.output_dir / "output_001.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_write_drop_down_using_layout_manager(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # layout manager
        l: PageLayout = SingleColumnLayout(page)

        # write TextField
        l.add(
            FixedColumnWidthTable(number_of_rows=3, number_of_columns=2)
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
            .add(CountryDropDownList(value="Belgium"))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # write
        file = self.output_dir / "output_002.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        compare_visually_to_ground_truth(file)


if __name__ == "__main__":
    unittest.main()
