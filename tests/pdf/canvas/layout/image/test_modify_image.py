import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from PIL import Image as PILImage

from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth


class TestModifyImage(unittest.TestCase):
    """
    This test creates a PDF with an Image in it, this is specified by a URL
    and then modifies that Image
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

    def _modify_image(self, image: PILImage.Image):
        w = image.width
        h = image.height
        pixels = image.load()
        for i in range(0, w):
            for j in range(0, h):
                r, g, b = pixels[i, j]

                # convert to sepia
                new_r = r * 0.393 + g * 0.769 + b * 0.189
                new_g = r * 0.349 + g * 0.686 + b * 0.168
                new_b = r * 0.272 + g * 0.534 + b * 0.131

                # set
                pixels[i, j] = (int(new_r), int(new_g), int(new_b))

    def test_write_document_with_image(self):

        # create empty document
        pdf: Document = Document()

        # create empty page
        page: Page = Page()

        # add page to document
        pdf.append_page(page)

        # add Image
        layout = SingleColumnLayout(page)

        # add test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with an Image in it."))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        # add image
        layout.add(
            Image(
                "https://images.unsplash.com/photo-1597826368522-9f4cb5a6ba48?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw",
                width=Decimal(256),
                height=Decimal(256),
                horizontal_alignment=Alignment.CENTERED,
            )
        )

        # write
        file = self.output_dir / "output_001.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    def test_modify_image_in_document(self):

        # read input
        doc = None
        with open(self.output_dir / "output_001.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # read images
        xobjects = doc["XRef"]["Trailer"]["Root"]["Pages"]["Kids"][0]["Resources"][
            "XObject"
        ]

        # modify image(s)
        for k, v in xobjects.items():
            if isinstance(v, PILImage.Image):
                self._modify_image(v)

        # write
        file = self.output_dir / "output_002.pdf"
        with open(file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")


if __name__ == "__main__":
    unittest.main()
