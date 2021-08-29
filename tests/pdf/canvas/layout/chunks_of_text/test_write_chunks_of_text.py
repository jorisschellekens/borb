import typing
import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor, Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteChunksOfText(unittest.TestCase):
    """
    This test creates a PDF with a Paragraph object in it. The Paragraph is aligned TOP, LEFT.
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

    def test_write_document_001(self):

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
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is composed of smaller heterogenous ChunkOfText objects."
                    "The Paragraph is aligned TOP, LEFT. The yellow box is the bounding box given to the layout algorithm."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        txt: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex"
        font_sizes: typing.List[Decimal] = [
            Decimal(20) if i % 5 == 4 else Decimal(12) for i in range(0, 5)
        ]
        fonts: typing.List[str] = [
            "Helvetica-Bold" if i % 7 == 6 else "Helvetica" for i in range(0, 7)
        ]
        colors: typing.List[Color] = [
            HexColor("f1cd2e") if i % 11 == 10 else HexColor("000000")
            for i in range(0, 11)
        ]

        words: typing.List[str] = txt.split(" ")
        chunks_of_text = [
            ChunkOfText(
                x + " ",
                font_size=font_sizes[i % len(font_sizes)],
                font=fonts[i % len(fonts)],
                font_color=colors[i % len(colors)],
            )
            for i, x in enumerate(words)
        ]

        bb = Rectangle(Decimal(59), Decimal(500), Decimal(476), Decimal(124))
        HeterogeneousParagraph(chunks_of_text).layout(page, bb)

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=HexColor("f1cd2e"),
            rectangle=bb,
        )

        # determine output location
        out_file = self.output_dir / "output_001.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_document_002(self):

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
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is composed of smaller heterogenous ChunkOfText objects."
                    "The Paragraph is aligned TOP, RIGHT. The yellow box is the bounding box given to the layout algorithm."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        txt: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex"
        font_sizes: typing.List[Decimal] = [
            Decimal(20) if i % 5 == 4 else Decimal(12) for i in range(0, 5)
        ]
        fonts: typing.List[str] = [
            "Helvetica-Bold" if i % 7 == 6 else "Helvetica" for i in range(0, 7)
        ]
        colors: typing.List[Color] = [
            HexColor("f1cd2e") if i % 11 == 10 else HexColor("000000")
            for i in range(0, 11)
        ]

        words: typing.List[str] = txt.split(" ")
        chunks_of_text = [
            ChunkOfText(
                x + " ",
                font_size=font_sizes[i % len(font_sizes)],
                font=fonts[i % len(fonts)],
                font_color=colors[i % len(colors)],
            )
            for i, x in enumerate(words)
        ]

        bb = Rectangle(Decimal(59), Decimal(500), Decimal(476), Decimal(124))
        HeterogeneousParagraph(
            chunks_of_text, horizontal_alignment=Alignment.RIGHT
        ).layout(page, bb)

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=HexColor("f1cd2e"),
            rectangle=bb,
        )

        # determine output location
        out_file = self.output_dir / "output_002.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_document_003(self):

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
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is composed of smaller heterogenous ChunkOfText objects."
                    "The Paragraph is aligned TOP, CENTERED. The yellow box is the bounding box given to the layout algorithm."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        txt: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex"
        font_sizes: typing.List[Decimal] = [
            Decimal(20) if i % 5 == 4 else Decimal(12) for i in range(0, 5)
        ]
        fonts: typing.List[str] = [
            "Helvetica-Bold" if i % 7 == 6 else "Helvetica" for i in range(0, 7)
        ]
        colors: typing.List[Color] = [
            HexColor("f1cd2e") if i % 11 == 10 else HexColor("000000")
            for i in range(0, 11)
        ]

        words: typing.List[str] = txt.split(" ")
        chunks_of_text = [
            ChunkOfText(
                x + " ",
                font_size=font_sizes[i % len(font_sizes)],
                font=fonts[i % len(fonts)],
                font_color=colors[i % len(colors)],
            )
            for i, x in enumerate(words)
        ]

        bb = Rectangle(Decimal(59), Decimal(500), Decimal(476), Decimal(124))
        HeterogeneousParagraph(
            chunks_of_text, horizontal_alignment=Alignment.CENTERED
        ).layout(page, bb)

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=HexColor("f1cd2e"),
            rectangle=bb,
        )

        # determine output location
        out_file = self.output_dir / "output_003.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_document_004(self):

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
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is composed of smaller heterogenous ChunkOfText objects."
                    "The Paragraph is aligned TOP, LEFT, with padding 10. The yellow box is the bounding box given to the layout algorithm."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        txt: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex"
        font_sizes: typing.List[Decimal] = [
            Decimal(20) if i % 5 == 4 else Decimal(12) for i in range(0, 5)
        ]
        fonts: typing.List[str] = [
            "Helvetica-Bold" if i % 7 == 6 else "Helvetica" for i in range(0, 7)
        ]
        colors: typing.List[Color] = [
            HexColor("f1cd2e") if i % 11 == 10 else HexColor("000000")
            for i in range(0, 11)
        ]

        words: typing.List[str] = txt.split(" ")
        chunks_of_text = [
            ChunkOfText(
                x + " ",
                font_size=font_sizes[i % len(font_sizes)],
                font=fonts[i % len(fonts)],
                font_color=colors[i % len(colors)],
            )
            for i, x in enumerate(words)
        ]

        bb = Rectangle(Decimal(59), Decimal(450), Decimal(476), Decimal(124))
        HeterogeneousParagraph(
            chunks_of_text,
            padding_top=Decimal(10),
            padding_right=Decimal(10),
            padding_bottom=Decimal(10),
            padding_left=Decimal(10),
        ).layout(page, bb)

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=HexColor("f1cd2e"),
            rectangle=bb,
        )

        # determine output location
        out_file = self.output_dir / "output_004.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)

    def test_write_document_005(self):

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
                    "This test creates a PDF with a Paragraph object in it. The Paragraph is composed of smaller heterogenous ChunkOfText objects."
                    "The Paragraph is aligned TOP, LEFT. The yellow box is the bounding box given to the layout algorithm."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        txt: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex"
        font_sizes: typing.List[Decimal] = [
            Decimal(20) if i % 5 == 4 else Decimal(12) for i in range(0, 5)
        ]
        fonts: typing.List[str] = [
            "Helvetica-Bold" if i % 7 == 6 else "Helvetica" for i in range(0, 7)
        ]
        colors: typing.List[Color] = [
            HexColor("f1cd2e") if i % 11 == 10 else HexColor("ffffff")
            for i in range(0, 11)
        ]

        words: typing.List[str] = txt.split(" ")
        chunks_of_text = [
            ChunkOfText(
                x + " ",
                font_size=font_sizes[i % len(font_sizes)],
                font=fonts[i % len(fonts)],
                font_color=colors[i % len(colors)],
            )
            for i, x in enumerate(words)
        ]

        bb = Rectangle(Decimal(59), Decimal(450), Decimal(476), Decimal(124))
        HeterogeneousParagraph(
            chunks_of_text,
            padding_top=Decimal(5),
            padding_right=Decimal(5),
            padding_bottom=Decimal(5),
            padding_left=Decimal(5),
            background_color=HexColor("0b3954"),
        ).layout(page, bb)

        # add rectangle annotation
        page.append_square_annotation(
            stroke_color=HexColor("f1cd2e"),
            rectangle=bb,
        )

        # determine output location
        out_file = self.output_dir / "output_005.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        compare_visually_to_ground_truth(out_file)
