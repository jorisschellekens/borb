import io
import typing
from decimal import Decimal

from PIL import Image as PILImage  # type: ignore [import]
import xml.etree.ElementTree as ET

from ptext.pdf.canvas.color.color import Color
from ptext.pdf.pdf import PDF
from ptext.toolkit.export.pdf_to_svg import PDFToSVG


class PDFToHTML(PDFToSVG):
    @staticmethod
    def convert_pdf_to_html(
        file: typing.Union[io.BufferedIOBase, io.RawIOBase], page_number: int
    ) -> ET.Element:
        l: "PDFToHTML" = PDFToHTML()
        with open(file, "rb") as pdf_file_handle:
            PDF.loads(pdf_file_handle, [l])
        return l.get_html(page_number)

    def __init__(self):
        super(PDFToHTML, self).__init__()
        self._html_per_page: typing.Dict[int, ET.Element] = {}

    def _begin_page(
        self, page_nr: Decimal, page_width: Decimal, page_height: Decimal
    ) -> None:
        self._html_per_page[page_nr] = ET.fromstring(
            "<html><head></head><body></body></html>"
        )

    def _render_image(
        self,
        page_nr: Decimal,
        page_width: Decimal,
        page_height: Decimal,
        x: Decimal,
        y: Decimal,
        image_width: Decimal,
        image_height: Decimal,
        image: PILImage,
    ):
        pass

    def _render_text(
        self,
        page_nr: Decimal,
        page_width: Decimal,
        page_height: Decimal,
        x: Decimal,
        y: Decimal,
        font_color: Color,
        font_size: Decimal,
        font_name: str,
        bold: bool,
        italic: bool,
        text: str,
    ):
        pass

    def get_html(self, page_nr: int) -> ET.Element:
        assert page_nr in self._html_per_page
        return self._html_per_page[page_nr]
