from decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Barcode
from borb.pdf import BarcodeType
from borb.pdf import ConnectedShape
from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import Image
from borb.pdf import OrderedList
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import Table
from borb.pdf import UnorderedList
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.layout.shape.progressbar import ProgressSquare
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from tests.test_case import TestCase


class TestNewLayoutMethods(TestCase):
    """
    This test attempts to insert the most common LayoutElements in a single PDF.
    """

    def test_create_dummy_pdf(self):
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
            Image(
                "https://images.unsplash.com/photo-1557804506-669a67965ba0",
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Image(
                "https://images.unsplash.com/photo-1523800503107-5bc3ba2a6f81",
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Image(
                "https://images.unsplash.com/photo-1544141310-d3b5a03ac5a8",
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Image(
                "https://images.unsplash.com/photo-1583190298857-df3010faeb95",
                width=Decimal(64),
                height=Decimal(64),
            )
        )
        t.add(
            Image(
                "https://images.unsplash.com/photo-1512138664757-360e0aad5132",
                width=Decimal(64),
                height=Decimal(64),
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
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, d)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
