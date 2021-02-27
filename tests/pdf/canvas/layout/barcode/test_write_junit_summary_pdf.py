import logging
import typing
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.barcode import Barcode, BarcodeType
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Justification,
    Paragraph,
)
from ptext.pdf.canvas.layout.shape import Shape
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-junit-summary-pdf.log", level=logging.DEBUG
)

import xml.etree.ElementTree as ET

import requests
from PIL import Image as PILImage


class TestWriteJUnitSummaryPDF(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../../output/test-write-junit-summary-pdf")

    def _write_logo(self, page: Page):
        image_url = "https://icons.iconarchive.com/icons/thesquid.ink/free-flat-sample/256/rubber-duck-icon.png"
        im = PILImage.open(requests.get(image_url, stream=True).raw)
        Image(im).layout(
            page,
            bounding_box=Rectangle(Decimal(20), Decimal(800), Decimal(49), Decimal(18)),
        )

    def _write_footer(self, page: Page):
        # footer
        rectangle_box = Rectangle(
            Decimal(0),
            Decimal(0),
            page.get_page_info().get_width(),
            page.get_page_info().get_height() * Decimal(0.05),
        )
        Shape(
            LineArtFactory.rectangle(rectangle_box),
            fill_color=HexColor("5dbb46"),
            stroke_color=HexColor("5dbb46"),
            line_width=Decimal(1),
        ).layout(page, rectangle_box)

        rectangle_box = Rectangle(
            Decimal(0),
            page.get_page_info().get_height() * Decimal(0.05),
            page.get_page_info().get_width(),
            Decimal(2),
        )
        Shape(
            LineArtFactory.rectangle(rectangle_box),
            fill_color=X11Color("SlateGray"),
            stroke_color=X11Color("SlateGray"),
            line_width=Decimal(1),
        ).layout(page, rectangle_box)

    def _write_page(self, doc: Document, results, from_index: int, to_index: int):
        page = Page()
        doc.append_page(page)

        # set layout manager
        layout = SingleColumnLayout(page)

        # create Table
        N = to_index - from_index
        table = Table(
            number_of_rows=N + 1,
            number_of_columns=5,
            column_widths=[Decimal(1), Decimal(2), Decimal(3), Decimal(2), Decimal(2)],
        )

        # logo
        self._write_logo(page)

        # header
        table.add(
            Paragraph("Nr.", font_color=HexColor("#5dbb46"), font_size=Decimal(20))
        )
        table.add(
            Paragraph("Category", font_color=HexColor("#5dbb46"), font_size=Decimal(20))
        )
        table.add(
            Paragraph("Name", font_color=HexColor("#5dbb46"), font_size=Decimal(20))
        )
        table.add(
            Paragraph("Time", font_color=HexColor("#5dbb46"), font_size=Decimal(20))
        )
        table.add(
            Paragraph("Status", font_color=HexColor("#5dbb46"), font_size=Decimal(20))
        )

        # iterate over results
        annotation_positions: typing.Dict[Paragraph, str] = {}
        for i, testcase in enumerate(results[from_index:to_index]):
            class_name = testcase.attrib.get("classname", "")
            name = testcase.attrib.get("name", "")
            time = round(Decimal(testcase.attrib.get("time", "0")), 2)
            fail = any([x.tag == "failure" for x in testcase])
            fail_message = next(
                iter(
                    [
                        x.attrib.get("message", "")
                        for x in testcase
                        if x.tag == "failure"
                    ]
                ),
                "",
            )

            table.add(Paragraph(str(i + from_index), font_size=Decimal(8)))
            table.add(Paragraph(class_name, font_size=Decimal(8)))
            table.add(Paragraph(name, font_size=Decimal(8)))
            table.add(
                Paragraph(
                    str(time),
                    font_size=Decimal(8),
                    justification=Justification.CENTERED,
                )
            )
            status_para = None
            if fail:
                status_para = Paragraph(
                    "X",
                    font_color=X11Color("Red"),
                    justification=Justification.CENTERED,
                )
            else:
                status_para = Paragraph(
                    "V",
                    font_color=X11Color("Green"),
                    justification=Justification.CENTERED,
                )
            table.add(status_para)
            annotation_positions[status_para] = fail_message

        table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        table.set_border_width_on_all_cells(Decimal(0.5))
        layout.add(table)

        # add text annotations for failed tests
        for p, s in annotation_positions.items():
            if s == "":
                continue
            page.append_text_annotation(
                rectangle=Rectangle(
                    p.get_bounding_box().x + Decimal(64),
                    p.get_bounding_box().y,
                    Decimal(16),
                    Decimal(16),
                ),
                contents=s,
            )

        # add footer
        self._write_footer(page)

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty Document
        doc = Document()

        # add page
        tree = ET.parse("/home/joris/Downloads/testsuite (1).xml")
        testsuite = tree.getroot()
        for i in range(0, len(testsuite), 30):
            self._write_page(doc, [x for x in testsuite], i, i + 30)

        # last page
        page: Page = Page()
        doc.append_page(page)
        layout = MultiColumnLayout(page)

        # add paragraph
        layout.add(
            Paragraph(
                "For more information go to jenkins.com, or scan the following qr code:",
                font="Helvetica-Bold",
            )
        )

        # add qr code
        layout.add(
            Barcode(
                data="https://jenkins.com",
                type=BarcodeType.QR,
                stroke_color=HexColor("#5dbb46"),
                width=Decimal(128),
            )
        )

        # footer
        self._write_footer(page)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)
