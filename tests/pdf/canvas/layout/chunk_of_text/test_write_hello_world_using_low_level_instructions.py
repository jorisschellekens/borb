import logging
import unittest
import zlib
from pathlib import Path

from ptext.io.read.types import Decimal as pDecimal
from ptext.io.read.types import Stream, Name, Dictionary
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF

logging.basicConfig(
    filename="../../../../logs/test-write-hello-world-low-level-using-low-level-instructions.log",
    level=logging.DEBUG,
)


class TestWriteHelloWorldUsingLowLevelInstructions(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            "../../../../output/test-write-hello-world-using-low-level-instructions"
        )

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # create content stream
        content_stream = Stream()
        content_stream[
            Name("DecodedBytes")
        ] = b"""
            q
            BT
            /F1 24 Tf            
            100 742 Td            
            (Hello World!) Tj
            ET
            Q
        """
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Filter")] = Name("FlateDecode")
        content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))

        # set content of page
        page[Name("Contents")] = content_stream

        # set Font
        page[Name("Resources")] = Dictionary()
        page["Resources"][Name("Font")] = Dictionary()
        page["Resources"]["Font"][Name("F1")] = Dictionary()
        page["Resources"]["Font"]["F1"][Name("Type")] = Name("Font")
        page["Resources"]["Font"]["F1"][Name("Subtype")] = Name("Type1")
        page["Resources"]["Font"]["F1"][Name("Name")] = Name("F1")
        page["Resources"]["Font"]["F1"][Name("BaseFont")] = Name("Helvetica")
        page["Resources"]["Font"]["F1"][Name("Encoding")] = Name("MacRomanEncoding")

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
