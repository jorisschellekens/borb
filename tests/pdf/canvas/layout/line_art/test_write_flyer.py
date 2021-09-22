import unittest
from pathlib import Path

import typing

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.image.barcode import Barcode, BarcodeType
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.image.shape import Shape
from borb.pdf.canvas.layout.layout_element import LayoutElement, Alignment
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document import Document
from borb.pdf.page.page import Page

from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestWriteFlyer(unittest.TestCase):
    """
    This test creates a PDF with a few PDF graphics in it
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

    def add_colored_artwork_bottom_right_corner(self, page: Page) -> None:
        """
        This method will add a blue/purple artwork of lines and squares to the bottom right corner
        of the given Page
        """
        ps: typing.Tuple[Decimal, Decimal] = PageSize.A4_PORTRAIT.value
        # square
        Shape(
            points=[
                (ps[0] - 32, 40),
                (ps[0], 40),
                (ps[0], 40 + 32),
                (ps[0] - 32, 40 + 32),
            ],
            stroke_color=HexColor("d53067"),
            fill_color=HexColor("d53067"),
        ).layout(page, Rectangle(ps[0] - 32, 40, 32, 32))
        # square
        Shape(
            points=[
                (ps[0] - 64, 40),
                (ps[0] - 32, 40),
                (ps[0] - 32, 40 + 32),
                (ps[0] - 64, 40 + 32),
            ],
            stroke_color=HexColor("eb3f79"),
            fill_color=HexColor("eb3f79"),
        ).layout(page, Rectangle(ps[0] - 64, 40, 32, 32))
        # triangle
        Shape(
            points=[
                (ps[0] - 96, 40),
                (ps[0] - 64, 40),
                (ps[0] - 64, 40 + 32),
            ],
            stroke_color=HexColor("e01b84"),
            fill_color=HexColor("e01b84"),
        ).layout(page, Rectangle(ps[0] - 96, 40, 32, 32))
        # line
        r: Rectangle = Rectangle(Decimal(0), Decimal(32), ps[0], Decimal(8))
        Shape(
            points=LineArtFactory.rectangle(r),
            stroke_color=HexColor("283592"),
            fill_color=HexColor("283592"),
        ).layout(page, r)

    def add_gray_artwork_upper_right_corner(self, page: Page) -> None:
        """
        This method will add a gray artwork of squares and triangles in the upper right corner
        of the given Page
        """
        grays: typing.List[HexColor] = [
            HexColor("A9A9A9"),
            HexColor("D3D3D3"),
            HexColor("DCDCDC"),
            HexColor("E0E0E0"),
            HexColor("E8E8E8"),
            HexColor("F0F0F0"),
        ]
        ps: typing.Tuple[Decimal, Decimal] = PageSize.A4_PORTRAIT.value
        N: int = 4
        M: Decimal = Decimal(32)
        for i in range(0, N):
            x: Decimal = ps[0] - N * M + i * M
            y: Decimal = ps[1] - (i + 1) * M
            rg: HexColor = grays[i % len(grays)]
            Shape(
                points=[(x + M, y), (x + M, y + M), (x, y + M)],
                stroke_color=rg,
                fill_color=rg,
            ).layout(page, Rectangle(x, y, M, M))
        for i in range(0, N - 1):
            for j in range(0, N - 1):
                if j > i:
                    continue
                x: Decimal = ps[0] - (N - 1) * M + i * M
                y: Decimal = ps[1] - (j + 1) * M
                rg: HexColor = grays[(i * 3 + j * 5) % len(grays)]
                Shape(
                    points=[(x, y), (x + M, y), (x + M, y + M), (x, y + M)],
                    stroke_color=rg,
                    fill_color=rg,
                ).layout(page, Rectangle(x, y, M, M))

    def test_create_flyer(self):

        # create empty Document
        pdf = Document()

        # create empty Page
        page = Page()

        # add Page to Document
        pdf.append_page(page)

        # create PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        # add artwork
        self.add_gray_artwork_upper_right_corner(page)

        # contact information
        layout.add(
            Paragraph(
                "Your Company", font_color=HexColor("#6d64e8"), font_size=Decimal(20)
            )
        )
        qr_code: LayoutElement = Barcode(
            data="https://www.borbpdf.com",
            width=Decimal(64),
            height=Decimal(64),
            type=BarcodeType.QR,
        )
        layout.add(
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=1)
            .add(qr_code)
            .add(
                Paragraph(
                    """
                500 South Buena Vista Street
                Burbank CA
                91521-0991 USA
                """,
                    padding_top=Decimal(12),
                    respect_newlines_in_text=True,
                    font_color=HexColor("#666666"),
                    font_size=Decimal(10),
                )
            )
            .no_borders()
        )
        page.append_remote_go_to_annotation(
            qr_code.get_bounding_box(), uri="https://www.borbpdf.com"
        )

        # title
        layout.add(
            Paragraph(
                "Productbrochure", font_color=HexColor("#283592"), font_size=Decimal(34)
            )
        )

        # subtitle
        layout.add(
            Paragraph(
                "September 4th, 2021",
                font_color=HexColor("#e01b84"),
                font_size=Decimal(11),
            )
        )

        # product overview
        layout.add(
            Paragraph(
                "Product Overview", font_color=HexColor("000000"), font_size=Decimal(21)
            )
        )
        layout.add(
            Paragraph(
                """
                Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. 
                Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. 
                A small river named Duden flows by their place and supplies it with the necessary regelialia.
                """,
                text_alignment=Alignment.JUSTIFIED,
            )
        )
        layout.add(
            Paragraph(
                """
                It is a paradisematic country, in which roasted parts of sentences fly into your mouth. 
                Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life. 
                One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar.
                """,
                text_alignment=Alignment.JUSTIFIED,
                margin_bottom=Decimal(12),
            )
        )

        # table with image and key features
        layout.add(
            FixedColumnWidthTable(
                number_of_rows=2,
                number_of_columns=2,
                column_widths=[Decimal(0.3), Decimal(0.7)],
            )
            .add(
                TableCell(
                    Image(
                        "https://www.att.com/catalog/en/skus/images/apple-iphone%2012-purple-450x350.png",
                        width=Decimal(128),
                        height=Decimal(128),
                    ),
                    row_span=2,
                )
            )
            .add(
                Paragraph(
                    "Key Features",
                    font_color=HexColor("e01b84"),
                    font="Helvetica-Bold",
                    padding_bottom=Decimal(10),
                )
            )
            # fmt: off
            .add(
                UnorderedList()
                .add(Paragraph("Nam aliquet ex eget felis lobortis aliquet sit amet ut risus."))
                .add(Paragraph("Maecenas sit amet odio ut erat tincidunt consectetur accumsan ut nunc."))
                .add(Paragraph("Phasellus eget magna et justo malesuada fringilla."))
                .add(Paragraph("Maecenas vitae dui ac nisi aliquam malesuada in consequat sapien."))
            )
            # fmt: on
            .no_borders()
        )

        self.add_colored_artwork_bottom_right_corner(page)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # check
        compare_visually_to_ground_truth(out_file)
