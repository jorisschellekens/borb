import copy
import typing

from borb.io.read.types import Decimal
from borb.pdf import ConnectedShape
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_case import TestCase


class TestAddChunksOfTextCheckBoundingBoxes(TestCase):
    """
    This test creates a PDF with a Paragraph object in it. The Paragraph is aligned TOP, LEFT.
    """

    def test_add_heterogeneousparagraph(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test creates a PDF with a Paragraph object in it. "
                "The Paragraph is composed of smaller heterogenous ChunkOfText objects."
            )
        )

        txt: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        words: typing.List[str] = txt.split(" ")
        colors: typing.List[Color] = [
            HexColor("f1cd2e") if i % 3 == 0 else HexColor("000000")
            for i in range(0, len(words))
        ]

        # build chunks_of_text
        chunks_of_text: typing.List[ChunkOfText] = [
            ChunkOfText(
                x + " ",
                font_color=colors[i],
            )
            for i, x in enumerate(words)
        ]

        bb = Rectangle(Decimal(59), Decimal(500), Decimal(476), Decimal(124))
        hp: HeterogeneousParagraph = HeterogeneousParagraph(chunks_of_text)
        hp.paint(page, bb)
        chunks_of_text = []
        for l in hp._split_to_lines_of_chunks_of_text(hp.get_previous_paint_box()):
            chunks_of_text.extend(l)

        # add rectangle annotation
        for i, c in enumerate(chunks_of_text):
            r: Rectangle = copy.deepcopy(chunks_of_text[i].get_previous_layout_box())
            r.y -= (i + 1) * Decimal(10)
            ConnectedShape(
                LineArtFactory.rectangle(r),
                stroke_color=colors[i],
                fill_color=colors[i],
            ).paint(page, r)

        with open(self.get_first_output_file(), "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
