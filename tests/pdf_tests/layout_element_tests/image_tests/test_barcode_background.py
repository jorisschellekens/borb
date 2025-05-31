import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.barcode import Barcode
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestBarcodeBackground(unittest.TestCase):

    def test_barcode_code_39_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="0123456789",
            barcode_type=Barcode.BarcodeType.CODE_39,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_code_39_background.pdf")

    def test_barcode_code_128_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="0123456789",
            barcode_type=Barcode.BarcodeType.CODE_128,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_code_128_background.pdf")

    def test_barcode_ean_8_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="0123456789",
            barcode_type=Barcode.BarcodeType.EAN_8,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_ean_8_background.pdf")

    def test_barcode_ean_13_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="012345678900",
            barcode_type=Barcode.BarcodeType.EAN_13,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_ean_13_background.pdf")

    def test_barcode_ean_14_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="0123456789000",
            barcode_type=Barcode.BarcodeType.EAN_14,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_ean_14_background.pdf")

    def test_barcode_issn_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="0123456789",
            barcode_type=Barcode.BarcodeType.ISSN,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_issn_background.pdf")

    def test_barcode_jan_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="450123456789",
            barcode_type=Barcode.BarcodeType.JAN,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_jan_background.pdf")

    def test_barcode_pzn_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="0123456789",
            barcode_type=Barcode.BarcodeType.PZN,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(80, 80),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_pzn_background.pdf")

    def test_barcode_upca_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Barcode(
            barcode_data="01234567890",
            barcode_type=Barcode.BarcodeType.UPCA,
            background_color=X11Color.YELLOW_MUNSELL,
            padding_top=10,
            padding_left=10,
            padding_right=10,
            padding_bottom=10,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_upca_background.pdf")
