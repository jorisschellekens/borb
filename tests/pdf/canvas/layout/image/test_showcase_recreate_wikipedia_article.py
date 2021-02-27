import logging
import unittest
from pathlib import Path

import requests
from PIL import Image as PILImage

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.list import UnorderedList
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-showcase-recreate-wikipedia-article.log",
    level=logging.DEBUG,
)


class TestShowcaseRecreateWikipediaArticle(unittest.TestCase):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            "../../../../output/test-showcase-recreate-wikipedia-article"
        )

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

        layout.add(
            Paragraph(
                "Rose",
                font_color=X11Color("MistyRose"),
                font_size=Decimal(20),
                font="Helvetica-Bold",
            )
        )
        layout.add(
            Paragraph(
                "A rose is a woody perennial flowering plant of the genus Rosa, in the family Rosaceae, or the flower it bears. "
                "There are over three hundred species and tens of thousands of cultivars. "
            )
        )
        layout.add(
            Paragraph(
                "They form a group of plants that can be erect shrubs, climbing, or trailing, with stems that are often armed with sharp prickles. "
                "Flowers vary in size and shape and are usually large and showy, "
                "in colours ranging from white through yellows and reds."
            )
        )
        layout.add(
            Paragraph(
                "Most species are native to Asia, with smaller numbers native to Europe, North America, and northwestern Africa. "
                "Species, cultivars and hybrids are all widely grown for their beauty and often are fragrant. "
            )
        )
        layout.add(
            Paragraph("Roses have acquired cultural significance in many societies. ")
        )
        layout.add(
            Paragraph(
                "Rose plants range in size from compact, miniature roses, to climbers that can reach seven meters in height. "
                "Different species hybridize easily, and this has been used in the development of the wide range of garden roses."
            )
        )

        # add image
        im = PILImage.open(
            requests.get(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                stream=True,
            ).raw
        )
        layout.add(Image(im, width=Decimal(256)))

        # add UnorderedList
        layout.add(Paragraph("The genus Rosa is subdivided into four subgenera:"))
        layout.add(
            UnorderedList()
            .add(Paragraph("Hulthemia", padding_bottom=Decimal(2)))
            .add(Paragraph("Hesperrhodos", padding_bottom=Decimal(2)))
            .add(Paragraph("Platyrhodon", padding_bottom=Decimal(2)))
            .add(Paragraph("Rosa", padding_bottom=Decimal(2)))
            .add(
                UnorderedList()
                .add(Paragraph("Banksianae"))
                .add(Paragraph("Bracteatae"))
                .add(Paragraph("Caninae"))
                .add(Paragraph("Carolinae"))
                .add(Paragraph("Chinensis"))
                .add(Paragraph("Gallicanae"))
                .add(Paragraph("Gymnocarpae"))
                .add(Paragraph("Laevigatae"))
                .add(Paragraph("Pimpinellifoliae"))
                .add(Paragraph("Rosa"))
                .add(Paragraph("Synstylae"))
            )
        )
        # write
        file = self.output_dir / "output.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

        return True


if __name__ == "__main__":
    unittest.main()
