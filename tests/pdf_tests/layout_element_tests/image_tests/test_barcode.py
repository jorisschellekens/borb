import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.barcode import Barcode
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestBarcode(unittest.TestCase):

    def test_barcode_code_39(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_code_39.pdf")

    def test_barcode_code_128(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_code_128.pdf")

    def test_barcode_ean_8(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_ean_8.pdf")

    def test_barcode_ean_13(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_ean_13.pdf")

    def test_barcode_ean_14(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_ean_14.pdf")

    def test_barcode_issn(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_issn.pdf")

    def test_barcode_jan(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_jan.pdf")

    def test_barcode_pzn(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_pzn.pdf")

    def test_barcode_upca(self):
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
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_barcode_upca.pdf")
