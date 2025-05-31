import unittest
import zlib

from borb.pdf import (
    Document,
    Page,
    PDF,
    SingleColumnLayout,
    PageLayout,
    Paragraph,
    A4Portrait,
)
from borb.pdf.primitives import name, hexstr, stream


class TestLayersOfAbstraction(unittest.TestCase):

    def test_build_pdf_using_low_level_api(self):

        # create a new Document
        document: Document = Document()

        # set up dictionaries
        # fmt: off
        document[name('XRef')] = {}
        document[name('Trailer')] = {}
        document[name('Trailer')][name('ID')] = [hexstr('EADE5ABA36B69F023EED7D4626DBA694'), hexstr('EADE5ABA36B69F023EED7D4626DBA694')]
        document[name('Trailer')][name('Info')] = {}
        document[name('Trailer')][name('Info')][name('CreationDate')] = "D:20250303223004+00'00'"
        document[name('Trailer')][name('Info')][name('ModDate')] = "D:20250303223004+00'00'"
        document[name('Trailer')][name('Info')][name('Producer')] = "borb"
        document[name('Trailer')][name('Root')] = {}
        document[name('Trailer')][name('Root')][name('Type')] = name('Catalog')
        document[name('Trailer')][name('Root')][name('Pages')] = {}
        # fmt: on

        # add a Page
        # fmt: off
        document[name('Trailer')][name('Root')][name('Pages')][name('Count')] = 1
        document[name('Trailer')][name('Root')][name('Pages')][name('Type')] = name('Pages')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')] = [{}]
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('CropBox')] = [0, 0, 595, 842]
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('MediaBox')] = [0, 0, 595, 842]
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('ProcSet')] = [name('PDF'), name('Text')]
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Rotate')] = 0
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Type')] = name('Page')
        # fmt: on

        # add some text
        # fmt: off
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Contents')] = stream()
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Contents')][name('Bytes')] = zlib.compress(b'q\nBT\n0.0 0.0 0.0 rg\n/F1 1 Tf\n12 0 0 12 59 744 Tm\n(Hello World!) Tj\nET\nQ\n')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Contents')][name('Filter')] = name('FlateDecode')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Contents')][name('Length')] = 86
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Contents')][name('Type')] = name('Stream')
        # fmt: on

        # add Font
        # fmt: off
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')] = {}
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')] = {}
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')][name('F1')] = {}
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')][name('F1')][name('Subtype')] = name('Type1')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')][name('F1')][name('Type')]  = name('Font')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')][name('F1')][name('BaseFont')] = name('Helvetica')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')][name('F1')][name('Encoding')] = name('WinAnsiEncoding')
        document[name('Trailer')][name('Root')][name('Pages')][name('Kids')][0][name('Resources')][name('Font')][name('F1')][name('Name')] = name('F1')
        # fmt: on

        # write
        PDF.write(
            what=document, where_to="assets/test_build_pdf_using_low_level_api.pdf"
        )

    def test_build_pdf_using_layout_element_paint(self):
        document: Document = Document()

        # add new Page
        page: Page = Page()
        document.append_page(page)

        # add Paragraph
        # note:     We need to provide the coordinates.
        #           So you get a lot of control, but you have to put in the effort.
        Paragraph(text="Hello World!").paint(
            available_space=(59, 84, 477, 674), page=page
        )

        # write
        PDF.write(
            what=document,
            where_to="assets/test_build_pdf_using_layout_element_paint.pdf",
        )

    def test_build_pdf_using_page_layout(self):
        document: Document = Document()

        # add new Page
        page: Page = Page()
        document.append_page(page)

        # set up a PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        # add Paragraph
        # note:     No more messing with coordinates!
        #           PageLayout takes care of padding, margin, etc
        layout.append_layout_element(Paragraph("Hello World!"))

        # write
        PDF.write(what=document, where_to="assets/test_build_pdf_using_page_layout.pdf")

    def test_build_pdf_using_template(self):
        A4Portrait().append_single_column_of_text("Hello World!").save(
            "assets/test_build_pdf_using_template.pdf"
        )
