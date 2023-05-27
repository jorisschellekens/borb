import copy
import unittest
from decimal import Decimal

from borb.io.read.types import Boolean as bBool
from borb.io.read.types import CanvasOperatorName
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary as bDict
from borb.io.read.types import Function
from borb.io.read.types import HexadecimalString
from borb.io.read.types import List as bList
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.read.types import String as bString
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import Page
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation
from borb.pdf.canvas.layout.annotation.link_annotation import DestinationType
from borb.pdf.canvas.layout.annotation.link_annotation import LinkAnnotation
from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation
from borb.pdf.page.page_info import PageInfo
from borb.pdf.trailer.document_info import DocumentInfo
from borb.pdf.xref.plaintext_xref import PlainTextXREF
from borb.pdf.xref.xref import XREF


class TestDeepCopyBorbTypes(unittest.TestCase):
    """
    This test checks whether a deepcopy of a borb primitive/object type
    returns an object of the same type.
    """

    #
    # PRIMITIVES
    #

    def test_deepcopy_string(self):
        s0: bString = bString("Hello World")
        s1 = copy.deepcopy(s0)
        assert isinstance(s1, bString)

    def test_deepcopy_hexadecimal_string(self):
        s0: HexadecimalString = HexadecimalString("00FF00")
        s1 = copy.deepcopy(s0)
        assert isinstance(s1, HexadecimalString)

    def test_deepcopy_decimal(self):
        d0: bDecimal = bDecimal(3.14)
        d1 = copy.deepcopy(d0)
        assert isinstance(d1, bDecimal)

    def test_deepcopy_bool(self):
        b0: bBool = bBool(True)
        b1 = copy.deepcopy(b0)
        assert isinstance(b1, bBool)

    def test_deepcopy_canvas_operator_name(self):
        b0: CanvasOperatorName = CanvasOperatorName("q")
        b1 = copy.deepcopy(b0)
        assert isinstance(b1, CanvasOperatorName)

    def test_deepcopy_name(self):
        b0: Name = Name("Info")
        b1 = copy.deepcopy(b0)
        assert isinstance(b1, Name)

    def test_deepcopy_reference(self):
        p0: Reference = Reference()
        p1 = copy.deepcopy(p0)
        assert isinstance(p1, Reference)

    #
    # COLLECTIONS
    #

    def test_deepcopy_list(self):
        b0: bList = bList()
        b1 = copy.deepcopy(b0)
        assert isinstance(b1, bList)

    def test_deepcopy_dict(self):
        b0: bDict = bDict()
        b1 = copy.deepcopy(b0)
        assert isinstance(b1, bDict)

    def test_deepcopy_stream(self):
        b0: Stream = Stream()
        b1 = copy.deepcopy(b0)
        assert isinstance(b1, Stream)

    def test_deepcopy_function(self):
        p0: Function = Function()
        p1 = copy.deepcopy(p0)
        assert isinstance(p1, Function)

    #
    # OBJECTS
    #

    def test_deepcopy_page(self):
        p0: Page = Page()
        p1 = copy.deepcopy(p0)
        assert isinstance(p1, Page)

    def test_deepcopy_font(self):
        f0: Font = StandardType1Font("Helvetica")
        f1 = copy.deepcopy(f0)
        assert isinstance(f1, Font)

    def test_deepcopy_document(self):
        d0: Document = Document()
        d1 = copy.deepcopy(d0)
        assert isinstance(d1, Document)

    def test_deepcopy_xref(self):
        x0: XREF = PlainTextXREF()
        x1 = copy.deepcopy(x0)
        assert isinstance(x1, XREF)
        assert isinstance(x1, PlainTextXREF)

    def test_deepcopy_canvas(self):
        c0: Canvas = Canvas()
        c1 = copy.deepcopy(c0)
        assert isinstance(c1, Canvas)

    def test_deepcopy_document_information(self):
        d0: Document = Document()
        c0: DocumentInfo = d0.get_document_info()
        c1 = copy.deepcopy(c0)
        assert isinstance(c1, DocumentInfo)

    def test_deepcopy_page_information(self):
        d0: Document = Document()
        p0: Page = Page()
        d0.add_page(Page())
        c0: PageInfo = p0.get_page_info()
        c1 = copy.deepcopy(c0)
        assert isinstance(c1, PageInfo)

    def test_deepcopy_square_annotation(self):
        a0: Annotation = SquareAnnotation(
            bounding_box=Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100)),
            fill_color=HexColor("ff0000"),
            stroke_color=HexColor("ff0000"),
        )
        a1 = copy.deepcopy(a0)
        assert isinstance(a1, Annotation)
        assert isinstance(a1, SquareAnnotation)

    def test_deepcopy_link_annotation(self):
        a0: Annotation = LinkAnnotation(
            bounding_box=Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100)),
            page=Decimal(0),
            destination_type=DestinationType.FIT,
        )
        a1 = copy.deepcopy(a0)
        assert isinstance(a1, Annotation)
        assert isinstance(a1, LinkAnnotation)
