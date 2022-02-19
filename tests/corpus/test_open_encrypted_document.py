import os
import typing
import unittest
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


class TestOpenEncryptedDocument(unittest.TestCase):
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

        # link to corpus
        self.corpus_dir: Path = Path("/home/joris/Code/pdf-corpus/password-protected")

        # (global) stats
        self.number_of_documents: int = 0
        self.number_of_passes: int = 0
        self.number_of_fails: int = 0
        self.memory_stats_per_document: typing.Dict[str, typing.Tuple[int, int]] = {}

    @unittest.skip
    def test_against_entire_corpus(self):
        pdf_file_names = os.listdir(self.corpus_dir)
        pdfs = [(self.corpus_dir / x) for x in pdf_file_names if x.endswith(".pdf")]
        self._test_list_of_documents(pdfs)
        plt.close("all")

    def test_open_document(self):
        self._test_list_of_documents(
            [Path("/home/joris/Code/pdf-corpus/password-protected/0221.pdf")]
        )

    def _test_list_of_documents(self, documents: typing.List[Path]):
        self.number_of_documents = len(documents)
        self.number_of_passes = 0
        self.number_of_fails = 0
        self.memory_stats_per_document = {}
        for i, doc in enumerate(documents):
            try:
                print("processing %s [%d/%d] ..." % (doc.stem, i + 1, len(documents)))
                with open(doc, "rb") as pdf_file_handle:
                    PDF.loads(pdf_file_handle)
                self.number_of_passes += 1
            except Exception as e:
                print("ERROR, document %s, %s" % (doc.name, str(e)))
                self.number_of_fails += 1
                pass
            self._build_document()

    def _build_document(self):

        doc: Document = Document()

        # append page
        page: Page = Page()
        doc.append_page(page)

        # add test information
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test attempts to read each PDF in a corpus of roughly 1000 PDF documents."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # graph with timing information
        labels = (
            "pass",
            "fail",
        )
        sizes = [self.number_of_passes, self.number_of_fails]
        explode = (
            0,
            0,
        )  # only "explode" the 2nd slice (i.e. '<1s')
        fig1, ax1 = plt.subplots()
        ax1.pie(
            sizes,
            explode=explode,
            labels=labels,
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
            colors=["#a5ffd6", "#56cbf9", "#0b3954", "#f1cd2e", "#de6449"],
        )
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        layout.add(
            Chart(
                plt.gcf(),
                width=Decimal(200),
                height=Decimal(200),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # raw data
        ul: UnorderedList = UnorderedList()
        ul.add(
            Paragraph(
                "processed %d documents"
                % (self.number_of_fails + self.number_of_passes)
            )
        )
        ul.add(
            Paragraph(
                "%d fail(s), %d pass(es)"
                % (self.number_of_fails, self.number_of_passes)
            )
        )
        layout.add(ul)

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # close figure(s)
        plt.close("all")
