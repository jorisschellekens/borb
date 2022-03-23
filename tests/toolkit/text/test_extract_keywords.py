import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.stop_words import ENGLISH_STOP_WORDS
from borb.toolkit.text.text_rank_keyword_extraction import TextRankKeywordExtraction
from borb.toolkit.text.tf_idf_keyword_extraction import TFIDFKeywordExtraction

import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractKeywords(unittest.TestCase):
    """
    This test attempts to extract the keywords (TF-IDF)
    from each PDF in the corpus
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

        # create document
        pdf = Document()

        # add page
        page = Page()
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
                    "This test creates a PDF with an empty Page, and a Paragraph of text. "
                    "A subsequent test will attempt to extract the keywords from this text."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        layout.add(
            Paragraph(
                """
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
            when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 
            It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
            and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
            """
            )
        )

        layout.add(
            Paragraph(
                """
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. 
            The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, 
            as opposed to using 'Content here, content here', making it look like readable English. 
            Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, 
            and a search for 'lorem ipsum' will uncover many web sites still in their infancy. 
            Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
            """
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_extract_keywords_using_tf_idf_from_document(self):

        with open(self.output_dir / "output_001.pdf", "rb") as pdf_file_handle:
            l = TFIDFKeywordExtraction(ENGLISH_STOP_WORDS)
            doc = PDF.loads(pdf_file_handle, [l])

        # create document
        pdf = Document()

        # add page
        page = Page()
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
                    "This test creates a PDF with an empty Page, and adds the keywords it found"
                    "in the previously made PDF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add list
        layout.add(Paragraph("Following keywords were found:"))
        ul: UnorderedList = UnorderedList()
        for k in l.get_keywords_for_page(0)[:5]:
            ul.add(Paragraph(k[0]))
        layout.add(ul)

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_extract_keywords_using_textrank_from_document(self):

        l = TextRankKeywordExtraction()
        with open(self.output_dir / "output_001.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle, [l])

        # create document
        pdf = Document()

        # add page
        page = Page()
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
                    "This test creates a PDF with an empty Page, and adds the keywords it found"
                    "in the previously made PDF."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add list
        layout.add(Paragraph("Following keywords were found:"))
        ul: UnorderedList = UnorderedList()
        for k in l.get_keywords_for_page(0)[:5]:
            ul.add(Paragraph(k[0]))
        layout.add(ul)

        # attempt to store PDF
        with open(self.output_dir / "output_003.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)


if __name__ == "__main__":
    unittest.main()
