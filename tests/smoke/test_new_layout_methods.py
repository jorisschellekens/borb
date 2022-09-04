import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf import (
    Document,
    Page,
    Paragraph,
    PDF,
    HexColor,
    SingleColumnLayout,
    PageLayout,
    Image,
    UnorderedList,
    Heading,
    Barcode,
    BarcodeType,
    ConnectedShape,
    FixedColumnWidthTable,
    Table,
    OrderedList,
    Alignment,
)
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.image.unsplash import Unsplash
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.layout.shape.progressbar import ProgressSquare
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestNewLayoutMethods(unittest.TestCase):
    """
    This test attempts to insert the most common LayoutElements in a single PDF.
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

    def test_new_layout_framework(self):
        d: Document = Document()

        # Page
        p: Page = Page()
        d.add_page(p)

        # layout
        l: PageLayout = SingleColumnLayout(p)

        # table
        t: Table = FixedColumnWidthTable(number_of_rows=7, number_of_columns=6)

        # progressbar
        t.add(ProgressSquare(0.0, horizontal_alignment=Alignment.CENTERED))
        t.add(ProgressSquare(0.2, horizontal_alignment=Alignment.CENTERED))
        t.add(ProgressSquare(0.4, horizontal_alignment=Alignment.CENTERED))
        t.add(ProgressSquare(0.6, horizontal_alignment=Alignment.CENTERED))
        t.add(ProgressSquare(0.8, horizontal_alignment=Alignment.CENTERED))
        t.add(ProgressSquare(1.0, horizontal_alignment=Alignment.CENTERED))

        # shape (line art)
        bb: Rectangle = Rectangle(Decimal(0), Decimal(0), Decimal(32), Decimal(32))
        t.add(
            ConnectedShape(
                LineArtFactory.cartoon_diamond(bb),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_document(bb),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.flowchart_paper_tape(bb),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.droplet(bb),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            ConnectedShape(
                LineArtFactory.n_pointed_star(bb, 7),
                stroke_color=HexColor("56cbf9"),
                fill_color=None,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        t.add(
            DisconnectedShape(
                LineArtFactory.EURion(bb),
                stroke_color=HexColor("56cbf9"),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # paragraph
        t.add(Paragraph("Lorem ipsum dolor sit amet"))
        t.add(Paragraph("Lorem ipsum dolor sit amet", font_size=Decimal(8)))
        t.add(Paragraph("Lorem ipsum dolor sit amet", font_color=HexColor("56cbf9")))
        t.add(Paragraph("Lorem ipsum dolor sit amet", font="Helvetica-Bold"))
        t.add(Paragraph("Lorem ipsum dolor sit amet", font="Helvetica-Oblique"))
        t.add(
            HeterogeneousParagraph(
                [
                    ChunkOfText("Lorem "),
                    ChunkOfText("ipsum ", font_color=HexColor("56cbf9")),
                    ChunkOfText("dolor ", font_size=Decimal(8)),
                    ChunkOfText("sit ", font="Helvetica-Bold"),
                    ChunkOfText("amet", font="Helvetica-Oblique"),
                ]
            )
        )

        # list
        t.add(
            UnorderedList()
            .add(Paragraph("Lorem"))
            .add(Paragraph("ipsum"))
            .add(Paragraph("dolor"))
        )
        t.add(
            UnorderedList()
            .add(Paragraph("Lorem", font_size=Decimal(8)))
            .add(Paragraph("ipsum", font_size=Decimal(8)))
            .add(UnorderedList().add(Paragraph("dolor", font_size=Decimal(8))))
        )
        t.add(
            OrderedList()
            .add(Paragraph("Lorem"))
            .add(Paragraph("ipsum"))
            .add(Paragraph("dolor"))
        )
        t.add(
            OrderedList()
            .add(Paragraph("Lorem", font_size=Decimal(8)))
            .add(Paragraph("ipsum", font_size=Decimal(8)))
            .add(OrderedList().add(Paragraph("dolor", font_size=Decimal(8))))
        )
        t.add(
            OrderedList()
            .add(Paragraph("Lorem"))
            .add(Paragraph("ipsum", font_color=HexColor("56cbf9")))
            .add(Paragraph("dolor"))
        )
        t.add(
            OrderedList()
            .add(Paragraph("Lorem"))
            .add(Paragraph("ipsum"))
            .add(Emojis.PINEAPPLE.value)
        )

        # image
        t.add(
            Image(
                "https://raw.githubusercontent.com/jorisschellekens/borb/master/logo/borb.jpeg",
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Unsplash.get_image(
                ["team", "building"], width=Decimal(64), height=Decimal(64)
            )
        )
        t.add(
            Unsplash.get_image(
                ["laptop", "code"], width=Decimal(64), height=Decimal(64)
            )
        )
        t.add(
            Unsplash.get_image(
                ["office", "building"], width=Decimal(64), height=Decimal(64)
            )
        )
        t.add(
            Unsplash.get_image(
                ["nature", "building"], width=Decimal(64), height=Decimal(64)
            )
        )
        t.add(
            Unsplash.get_image(
                ["water", "nature"], width=Decimal(64), height=Decimal(64)
            )
        )

        # emoji
        t.add(Emojis.ARROW_DOUBLE_UP.value)
        t.add(Emojis.BIRD.value)
        t.add(Emojis.BALLOON.value)
        t.add(Emojis.MONEYBAG.value)
        t.add(Emojis.BLUE_DIAMOND.value)
        t.add(Emojis.SMILE.value)

        # chart
        # TODO

        # barcode
        t.add(Barcode("123456", BarcodeType.QR, width=Decimal(64), height=Decimal(64)))
        t.add(
            Barcode("1234567", BarcodeType.EAN_8, width=Decimal(64), height=Decimal(64))
        )
        t.add(
            Barcode(
                "1234567890123",
                BarcodeType.EAN_14,
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Barcode(
                "1234567890123",
                BarcodeType.CODE_39,
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Barcode(
                "1234567890123",
                BarcodeType.CODE_128,
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Barcode(
                "1234567890123",
                BarcodeType.ISBN_10,
                width=Decimal(64),
                height=Decimal(64),
            )
        )

        # padding
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        l.add(t)

        # determine output location
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, d)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
