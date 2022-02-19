import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.datastructure.str_trie import Trie
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.hyphenation.hyphenation import (
    Hyphenation,
)
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteHyphenatedParagraph(unittest.TestCase):
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

    def test_write_document_001(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)

        # write test info
        page_layout.add(
            Table(
                number_of_columns=2,
                number_of_rows=3,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a paragraph that will be hyphenated."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        hyph: Hyphenation = Hyphenation("en-gb")

        page_layout.add(
            Paragraph(
                "Without hyphenation",
                font_size=Decimal(20),
                font_color=HexColor("f1cd2e"),
            )
        )
        page_layout.add(
            Paragraph(
                """
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
        when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
        It has survived not only five centuries, but also the leap into electronic typesetting, 
        remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
        and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """
            )
        )

        page_layout.add(
            Paragraph(
                "With hyphenation", font_size=Decimal(20), font_color=HexColor("f1cd2e")
            )
        )
        page_layout.add(
            Paragraph(
                """
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
        when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
        It has survived not only five centuries, but also the leap into electronic typesetting, 
        remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
        and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """,
                hyphenation=hyph,
            )
        )

        # write
        file = self.output_dir / "output_001.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_001.pdf")

    def test_write_document_002(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        page_layout: PageLayout = SingleColumnLayout(page)

        # write test info
        page_layout.add(
            Table(
                number_of_columns=2,
                number_of_rows=3,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a paragraph that will be hyphenated."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        hyph: Hyphenation = Hyphenation("en-gb")
        page_layout.add(
            Paragraph(
                """
                Still others clutched their children closely to their breasts. One girl stood alone, slightly apart from the rest.
                She was quite young, not more than eighteen.
                """,
                hyphenation=hyph,
            )
        )

        # write
        file = self.output_dir / "output_002.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")

    def test_hyphenate_base_case_001(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 0
        Hyphenation.DO_NOT_HYPHENATE_AFTER = 0
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "a-a-a-a-a-a-a"

    def test_hyphenate_base_case_002(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 1
        Hyphenation.DO_NOT_HYPHENATE_AFTER = 32
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "aa-a-a-a-a-a"

    def test_hyphenate_base_case_003(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 0
        Hyphenation.DO_NOT_HYPHENATE_AFTER = -1
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "a-a-a-a-a-aa"

    def test_hyphenate_base_case_004(self):

        hyph: Hyphenation = Hyphenation("en-gb")

        # we are going to overwrite these private values
        # to ensure we know exactly where the split would happend
        hyph._patterns: Trie = Trie()
        hyph._patterns["a0a"] = 9
        hyph._exceptions = []
        hyph._min_prefix_length = 1
        hyph._max_prefix_length = 1
        hyph._min_suffix_length = 1
        hyph._max_suffix_length = 1

        Hyphenation.DO_NOT_HYPHENATE_BEFORE = 1
        Hyphenation.DO_NOT_HYPHENATE_AFTER = -1
        s: str = hyph.hyphenate("aaaaaaa", "-")
        assert s == "aa-a-a-a-aa"


if __name__ == "__main__":
    unittest.main()
