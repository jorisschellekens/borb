import os
import typing
import unittest
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from ptext.io.read.types import Decimal
from ptext.pdf.canvas.layout.image.chart import Chart
from ptext.pdf.canvas.layout.page_layout import PageLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF


class TestOpenDocument(unittest.TestCase):
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
        self.corpus_dir: Path = Path("/home/joris/Code/pdf-corpus/")

        # (global) stats
        self.number_of_documents: int = 0
        self.number_of_passes: int = 0
        self.number_of_fails: int = 0
        self.memory_stats_per_document: typing.Dict[str, typing.Tuple[int, int]] = {}

    def test_against_entire_corpus(self):
        pdf_file_names = os.listdir(self.corpus_dir)
        pdfs = [
            (self.corpus_dir / x)
            for x in pdf_file_names
            if x.endswith(".pdf") and "page_0" in x and (x not in ["0566_page_0.pdf"])
        ]
        self._test_list_of_documents(pdfs)
        plt.close("all")

    @unittest.skip
    def test_single_document(self):
        with open(self.corpus_dir / "0188_page_0.pdf", "rb") as fh:
            PDF.loads(fh)

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
                print(e)
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
        )
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        layout.add(Chart(plt.gcf()))

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # close figure(s)
        plt.close("all")
