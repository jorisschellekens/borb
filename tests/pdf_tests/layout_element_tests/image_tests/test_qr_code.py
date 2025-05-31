import unittest

from borb.pdf.document import Document
from borb.pdf.layout_element.image.qr_code import QRCode
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestQRCode(unittest.TestCase):

    def test_qr_code_micro(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        QRCode(
            qr_code_data="borbpdf.com",
            qr_code_type=QRCode.QRCodeType.MICRO,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_qr_code_micro.pdf")

    def test_qr_code_regular(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        QRCode(
            qr_code_data="http://borbpdf.com/",
            qr_code_type=QRCode.QRCodeType.REGULAR,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_qr_code_regular.pdf")
