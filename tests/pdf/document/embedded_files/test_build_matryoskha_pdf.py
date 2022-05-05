import io
import typing
import unittest
from decimal import Decimal
from pathlib import Path

from borb.pdf import PageLayout, Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator

unittest.TestLoader.sortTestMethodsUsing = None


class TestBuildMatryoshkaPDF(unittest.TestCase):
    """
    This test creates a PDF with a Paragraph object in it.
    An embedded file will later be added to this PDF.
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

    def _build_embedded_pdf(
        self, path_to_image: str, embedded_bytes: typing.Optional[bytes]
    ) -> bytes:
        doc: Document = Document()

        # create Page
        page: Page = Page()
        doc.append_page(page)

        # layout
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            Image(
                path_to_image,
                width=Decimal(128),
                height=Decimal(128),
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            )
        )

        # nesting
        if embedded_bytes is not None:
            doc.append_embedded_file("next-level.pdf", embedded_bytes)

        # to bytes
        buffer = io.BytesIO()
        PDF.dumps(buffer, doc)
        buffer.seek(0)

        # bytes
        return buffer.getvalue()

    def test_build_document(self):

        doc: Document = Document()

        # create Page
        page: Page = Page()
        doc.append_page(page)

        # layout
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            Image(
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/Adventure-Map-icon.png",
                width=Decimal(128),
                height=Decimal(128),
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            )
        )

        # embedded file
        to_embed: typing.Optional[bytes] = None
        for url in reversed(
            [
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/Castle-icon.png",
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/King-icon.png",
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/Viking-icon.png",
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/Knight-icon.png",
                "https://icons.iconarchive.com/icons/chanut/role-playing/128/Villager-icon.png",
            ]
        ):
            to_embed = self._build_embedded_pdf(url, to_embed)
        assert to_embed is not None
        doc.append_embedded_file("next-level.pdf", to_embed)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
