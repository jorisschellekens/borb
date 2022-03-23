import typing
import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_paragraph_extraction import SimpleParagraphExtraction
from tests.test_util import compare_visually_to_ground_truth


class TestSimpleParagraphExtraction(unittest.TestCase):
    """
    This test creates a PDF with an unsplash Image in it
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

    def test_write_document(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add Image
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a Paragraph in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        layout.add(
            Paragraph(
                """
        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, 
        eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. 
        Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, 
        sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. 
        Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
        sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
        Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? 
        Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, 
        vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
        """,
                font_size=Decimal(8),
            )
        )

        # write
        file = self.output_dir / "output_000.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_simple_paragraph_extraction(self):

        # read document
        l: SimpleParagraphExtraction = SimpleParagraphExtraction(
            maximum_multiplied_leading=Decimal(1.7)
        )
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output_000.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l])

        assert doc is not None

        # add SquareAnnotation(s)
        for p in l.get_paragraphs_for_page(0):
            doc.get_page(0).append_annotation(
                SquareAnnotation(p.get_bounding_box(), stroke_color=HexColor("f1cd2e"))
            )

        # write
        file = self.output_dir / "output_001.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # compare
        compare_visually_to_ground_truth(file)


if __name__ == "__main__":
    unittest.main()
