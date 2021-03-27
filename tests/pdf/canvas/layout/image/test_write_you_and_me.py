import logging
import unittest
from pathlib import Path

from PIL import Image as PILImage

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-you-and-me.log"), level=logging.DEBUG
)


class TestWriteYouAndMe(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-you-and-me")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add Image
        layout = MultiColumnLayout(page)

        # add image
        layout.add(
            Image(
                "https://images.unsplash.com/photo-1550155864-3033f844da36?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80",
                width=Decimal(256),
            )
        )
        layout.switch_to_next_column()

        # add title
        layout.add(
            Paragraph(
                "Love you more",
                font_color=X11Color("Crimson"),
                font="Helvetica-Bold",
                font_size=Decimal(20),
            )
        )
        layout.add(
            Paragraph(
                """When I say I love you more,
                                I don't just mean I love you more
                                than you love me. I mean I love
                                you more than the bad days
                                ahead of us. I love you more
                                than any fight we will ever have.
                                I love you more than the distance between us.
                                I love you more than any obstacle that
                                could ever try and come
                                between us. I love you the most.
                                """,
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """yours, most sincerely
                                JS
                             """,
                font_color=X11Color("SlateGray"),
                font="Helvetica-Bold",
                font_size=Decimal(8),
                respect_newlines_in_text=True,
            )
        )

        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
