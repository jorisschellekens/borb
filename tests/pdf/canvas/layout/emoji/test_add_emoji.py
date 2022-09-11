import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf import SingleColumnLayout, PageLayout, HexColor
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddEmoji(unittest.TestCase):
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

    def test_write_document(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.add_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)

        # write test info
        page_layout.add(
            FixedColumnWidthTable(
                number_of_columns=2,
                number_of_rows=3,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an emoji in it. This test uses the Emojis enum, which conveniently holds a wide range of images mapped to their emoji-name."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        page_layout.add(
            HeterogeneousParagraph(
                [
                    ChunkOfText(
                        "It wasn't easy. But borb now offers (basic) support for "
                    ),
                    Emojis.SMILEY.value,
                    ChunkOfText(". "),
                ]
            )
        )

        page_layout.add(
            HeterogeneousParagraph(
                [
                    ChunkOfText("Find out more on the "),
                    Emojis.OCTOCAT.value,
                    ChunkOfText("-repo."),
                ]
            )
        )

        page_layout.add(
            Paragraph(
                "If you are working with a font that does not offer (color) emoji, you can now ask borb to insert the image corresponding to the emoji of your choice. Emoji offer some convenience methods to make it easier to interact with them as if they were text, rather than images."
            )
        )

        # write
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)


if __name__ == "__main__":
    unittest.main()
