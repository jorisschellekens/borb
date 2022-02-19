import os
import time
import typing
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import matplotlib.pyplot as plt

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


class TestExtractTextExpectGroundTruth(unittest.TestCase):
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
        self.time_per_document: typing.Dict[str, float] = {}
        self.fails_per_document: typing.Dict[str, int] = []

    @unittest.skip
    def test_against_entire_corpus(self):
        pdf_file_names = os.listdir(self.corpus_dir)
        pdfs = [
            (self.corpus_dir / x)
            for x in pdf_file_names
            if x.endswith(".pdf") and "page_0" in x and (x not in ["0566_page_0.pdf"])
        ]
        self._test_list_of_documents(pdfs)
        plt.close("all")

    def _test_list_of_documents(self, documents: typing.List[Path]):
        self.number_of_documents = len(documents)
        self.number_of_passes = 0
        self.number_of_fails = 0
        self.time_per_document = {}
        self.fails_per_document = {}
        for i, doc in enumerate(documents):
            try:
                delta: float = time.time()
                print("processing %s [%d/%d] ..." % (doc.stem, i + 1, len(documents)))
                differences: typing.Dict[str, int] = self._test_single_document(doc)
                delta = time.time() - delta
                if len(differences) == 0:
                    self.number_of_passes += 1
                    self.time_per_document[doc.stem] = delta
                    self.fails_per_document[doc.stem] = 0
                else:
                    self.number_of_fails += 1
                    self.fails_per_document[doc.stem] = sum(
                        [abs(v) for k, v in differences.items()]
                    )
            except Exception as ex:
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
                    "This test attempts to read a corpus of roughly 1000 PDF documents, comparing the extracted text against the ground truth."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        graph_table: Table = Table(
            number_of_rows=2,
            number_of_columns=2,
            margin_top=Decimal(5),
            margin_bottom=Decimal(5),
        )
        graph_table.add(
            Paragraph(
                "Timing Information",
                font_color=HexColor("72A276"),
                font_size=Decimal(14),
                font="Helvetica-Bold",
            )
        )
        graph_table.add(
            Paragraph(
                "Failure Information",
                font_color=HexColor("72A276"),
                font_size=Decimal(14),
                font="Helvetica-Bold",
            )
        )

        # graph with timing information
        labels = "<1s", "<5s", "<10s", "<30s", ">30s"
        sizes = [
            sum([1 for k, v in self.time_per_document.items() if v < 1]),
            sum([1 for k, v in self.time_per_document.items() if 1 <= v < 5]),
            sum([1 for k, v in self.time_per_document.items() if 5 <= v < 10]),
            sum([1 for k, v in self.time_per_document.items() if 10 <= v < 30]),
            sum([1 for k, v in self.time_per_document.items() if v >= 30]),
        ]
        explode = (0.1, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. '<1s')
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
        graph_table.add(Chart(plt.gcf(), width=Decimal(128), height=Decimal(128)))

        # graph with error information
        labels = (
            "pass",
            "fail (<5 chars)",
            "fail (<10 chars)",
            "fail (<30 chars)",
            "fail (>30 chars)",
        )
        sizes = [
            sum([1 for k, v in self.fails_per_document.items() if v == 0]),
            sum([1 for k, v in self.fails_per_document.items() if 0 < v < 5]),
            sum([1 for k, v in self.fails_per_document.items() if 5 <= v < 10]),
            sum([1 for k, v in self.fails_per_document.items() if 10 <= v < 30]),
            sum([1 for k, v in self.fails_per_document.items() if v >= 30]),
        ]
        explode = (0.1, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. '<1s')
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
        graph_table.add(Chart(plt.gcf(), width=Decimal(128), height=Decimal(128)))
        graph_table.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        graph_table.no_borders()
        layout.add(graph_table)

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
        avg_processing_time: float = 0
        if len(self.time_per_document) > 0:
            avg_processing_time = sum(
                [v for k, v in self.time_per_document.items()]
            ) / len(self.time_per_document)
        ul.add(Paragraph("avg. processing time: %f seconds" % avg_processing_time))

        max_processing_time: float = 0
        if len(self.time_per_document) > 0:
            max_processing_time = max([v for k, v in self.time_per_document.items()])
        ul.add(Paragraph("max. processing time: %f seconds" % max_processing_time))

        min_processing_time: float = 0
        if len(self.time_per_document) > 0:
            min_processing_time = min([v for k, v in self.time_per_document.items()])
        ul.add(Paragraph("min. processing time: %f seconds" % min_processing_time))

        layout.add(ul)

        # tables processing
        if len(self.time_per_document) >= 5:

            # table of "wrongest" documents
            tmp = [(k, v) for k, v in self.fails_per_document.items()]
            tmp.sort(key=lambda x: x[1], reverse=True)
            tmp = tmp[0:5]
            t: Table = Table(
                number_of_columns=2,
                number_of_rows=7,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            t.add(
                TableCell(
                    Paragraph(
                        "Most Error-prone Documents",
                        font_color=HexColor("72A276"),
                        font="Helvetica-Bold",
                        font_size=Decimal(14.2),
                    ),
                    col_span=2,
                )
            )
            t.add(Paragraph("Document", font="Helvetica-Bold"))
            t.add(Paragraph("Number of errors", font="Helvetica-Bold"))
            for (k, v) in tmp:
                t.add(Paragraph(k))
                t.add(Paragraph(str(v)))
            t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            layout.add(t)

            # table of slowest documents
            tmp = [(k, v) for k, v in self.time_per_document.items()]
            tmp.sort(key=lambda x: x[1], reverse=True)
            tmp = tmp[0:5]
            t: Table = Table(
                number_of_columns=2,
                number_of_rows=7,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            t.add(
                TableCell(
                    Paragraph(
                        "Slowest Documents",
                        font_color=HexColor("72A276"),
                        font_size=Decimal(14.2),
                        font="Helvetica-Bold",
                    ),
                    col_span=2,
                )
            )
            t.add(Paragraph("Document", font="Helvetica-Bold"))
            t.add(Paragraph("Time (seconds)", font="Helvetica-Bold"))
            for (k, v) in tmp:
                t.add(Paragraph(k))
                t.add(Paragraph(str(v)))
            t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            layout.add(t)

            # table of fastest documents
            tmp = [(k, v) for k, v in self.time_per_document.items()]
            tmp.sort(key=lambda x: x[1])
            tmp = tmp[0:5]
            t: Table = Table(
                number_of_columns=2,
                number_of_rows=7,
                margin_top=Decimal(5),
                margin_bottom=Decimal(5),
            )
            t.add(
                TableCell(
                    Paragraph(
                        "Fastest Documents",
                        font_color=HexColor("72A276"),
                        font_size=Decimal(14),
                        font="Helvetica-Bold",
                    ),
                    col_span=2,
                )
            )
            t.add(Paragraph("Document", font="Helvetica-Bold"))
            t.add(Paragraph("Time (seconds)", font="Helvetica-Bold"))
            for (k, v) in tmp:
                t.add(Paragraph(k))
                t.add(Paragraph(str(v)))
            t.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            layout.add(t)

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # close figure(s)
        plt.close("all")

    def _test_single_document(self, file) -> typing.Dict[str, int]:

        txt_001 = ""
        try:
            with open(self.corpus_dir / (file.stem + ".txt"), "r") as fh_001:
                txt_001 = fh_001.read()
        except:
            pass

        txt_002: str = ""
        with open(file, "rb") as fh_002:
            l = SimpleTextExtraction()
            doc = PDF.loads(fh_002, [l])
            txt_002 = l.get_text_for_page(0)

        differences: typing.Dict[str, int] = {}
        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            count_001 = sum([1 if c == char else 0 for c in txt_001])
            count_002 = sum([1 if c == char else 0 for c in txt_002])
            if count_001 != count_002:
                differences[char] = count_001 - count_002

        # return
        return differences


if __name__ == "__main__":
    unittest.main()
