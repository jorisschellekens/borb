import unittest
from datetime import datetime
from pathlib import Path

from borb.pdf.canvas.layout.annotation.sound_annotation import SoundAnnotation

from borb.io.read.types import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.pdf import PDF


class TestAddSoundAnnotation(unittest.TestCase):
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

    def test_add_sound_annotation_001(self):

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
                    "This test creates a PDF with an empty Page, and an Image. A sound annotation is then added."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add image
        img: Image = Image(
            "https://images.unsplash.com/photo-1513883049090-d0b7439799bf",
            width=Decimal(128),
            height=Decimal(128),
        )
        layout.add(img)

        # add sound annotation
        page.append_annotation(
            SoundAnnotation(
                img.get_bounding_box(), "/home/joris/Downloads/audioclip.mp3"
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_add_sound_annotation_002(self):

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
                    "This test creates a PDF with an empty Page, and an Image. A sound annotation is then added."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add image
        img: Image = Image(
            "https://images.unsplash.com/photo-1513883049090-d0b7439799bf",
            width=Decimal(128),
            height=Decimal(128),
        )
        layout.add(img)

        # add sound annotation
        page.append_annotation(
            SoundAnnotation(
                img.get_bounding_box(),
                "https://commons.wikimedia.org/wiki/File:Variations_for_flute_and_piano.mp3",
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)
