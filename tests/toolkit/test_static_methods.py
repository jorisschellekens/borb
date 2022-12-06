import random
import typing
import unittest
from pathlib import Path

from borb.pdf import Lipsum, PageLayout, Color, HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit import (
    ColorExtraction,
    SimpleLineOfTextExtraction,
    SimpleParagraphExtraction,
    TextRankKeywordExtraction,
    TFIDFKeywordExtraction,
    RegularExpressionTextExtraction, PDFToSVG, PDFToJPG, PDFToMP3,
)
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction

unittest.TestLoader.sortTestMethodsUsing = None


class TestStaticMethods(unittest.TestCase):
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

    def test_create_document(self):
        doc: Document = Document()

        pge: Page = Page()
        doc.add_page(pge)

        lay: PageLayout = SingleColumnLayout(pge)

        random.seed(2048)
        colors: typing.List[Color] = [
            HexColor("#3A606E"),
            HexColor("#607B7D"),
            HexColor("#828E82"),
            HexColor("#AAAE8E"),
        ]
        fonts: typing.List[Font] = [
            StandardType1Font("Helvetica"),
            StandardType1Font("Helvetica-Bold"),
            StandardType1Font("Courier"),
            StandardType1Font("Courier-Bold"),
        ]
        for i in range(0, 4):
            lay.add(
                Paragraph(
                    Lipsum.generate_agatha_christie_text(random.choice([3, 4, 5])),
                    font=fonts[i],
                    font_color=colors[i],
                )
            )

        with open(self.output_dir / "output.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

    def test_get_colors(self):
        l: ColorExtraction = ColorExtraction()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        d0 = {k.to_rgb().to_hex_string(): v for k, v in l.get_color()[0].items()}
        d1 = {
            k.to_rgb().to_hex_string(): v
            for k, v in ColorExtraction.get_color_from_pdf(doc)[0].items()
        }
        for k, v in d0.items():
            assert k in d1
            assert v == d1[k]

    def test_get_fonts(self):
        # TODO
        pass

    def test_get_font_names(self):
        # TODO
        pass

    def test_get_images(self):
        # TODO
        pass

    def test_convert_to_jpg(self):
        l: PDFToJPG = PDFToJPG()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        assert l.convert_to_jpg()[0] == PDFToJPG.convert_pdf_to_jpg(doc)[0]

    @unittest.skip
    def test_convert_to_mp3(self):
        l: PDFToMP3 = PDFToMP3()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        assert l.convert_to_mp3()[0] == PDFToMP3.convert_pdf_to_mp3(doc)[0]

    def test_convert_to_svg(self):
        import xml.etree.ElementTree as ET
        l: PDFToSVG = PDFToSVG()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        assert ET.tostring(l.convert_to_svg()[0]) == ET.tostring(PDFToSVG.convert_pdf_to_svg(doc)[0])

    def test_get_matches(self):
        l: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Poirot")
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        l0 = l.get_matches()[0]
        l1 = RegularExpressionTextExtraction.get_matches_for_pdf("Poirot", doc)[0]
        for m in l0:
            assert (
                len(
                    [
                        x
                        for x in l1
                        if x.string == m.string
                        and x.get_font_color().to_rgb().to_hex_string()
                        == m.get_font_color().to_rgb().to_hex_string()
                        and x.get_bounding_boxes()[0].get_x()
                        == m.get_bounding_boxes()[0].get_x()
                        and x.get_bounding_boxes()[0].get_y()
                        == m.get_bounding_boxes()[0].get_y()
                    ]
                )
                >= 1
            )

    def test_get_lines_of_text(self):
        l: SimpleLineOfTextExtraction = SimpleLineOfTextExtraction()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        l0 = l.get_lines_of_text()[0]
        l1 = SimpleLineOfTextExtraction.get_lines_of_text_from_pdf(doc)[0]
        for lineOfText in l0:
            assert (
                len(
                    [
                        x
                        for x in l1
                        if x.get_text() == lineOfText.get_text()
                        and x.get_font_color().to_rgb().to_hex_string()
                        == lineOfText.get_font_color().to_rgb().to_hex_string()
                    ]
                )
                >= 1
            )

    def test_get_text(self):
        l: SimpleTextExtraction = SimpleTextExtraction()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        assert l.get_text()[0] == SimpleTextExtraction.get_text_from_pdf(doc)[0]

    def test_get_paragraphs(self):
        l: SimpleParagraphExtraction = SimpleParagraphExtraction()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        l0 = l.get_paragraphs()[0]
        l1 = SimpleParagraphExtraction.get_paragraphs_from_pdf(doc)[0]
        for lineOfText in l0:
            assert (
                len(
                    [
                        x
                        for x in l1
                        if x.get_text() == lineOfText.get_text()
                        and x.get_font_color().to_rgb().to_hex_string()
                        == lineOfText.get_font_color().to_rgb().to_hex_string()
                    ]
                )
                >= 1
            )

    def test_get_keywords_001(self):
        l: TextRankKeywordExtraction = TextRankKeywordExtraction()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        assert (
            l.get_keywords()[0]
            == TextRankKeywordExtraction.get_keywords_from_pdf(doc)[0]
        )

    def test_get_keywords_002(self):
        l: TFIDFKeywordExtraction = TFIDFKeywordExtraction()
        doc: typing.Optional[Document] = None
        with open(self.output_dir / "output.pdf", "rb") as fh:
            doc = PDF.loads(fh, [l])
        assert doc is not None
        assert (
            l.get_keywords()[0] == TFIDFKeywordExtraction.get_keywords_from_pdf(doc)[0]
        )
