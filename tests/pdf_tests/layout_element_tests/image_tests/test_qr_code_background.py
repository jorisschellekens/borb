import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.qr_code import QRCode
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestQRCodeBackground(unittest.TestCase):

    def test_qr_code_micro_background(self):
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

        PDF.write(what=d, where_to="assets/test_qr_code_micro_background.pdf")

    def test_qr_code_regular_background(self):
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

        PDF.write(what=d, where_to="assets/test_qr_code_regular_background.pdf")
