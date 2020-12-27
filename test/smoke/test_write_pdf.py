from pathlib import Path

from ptext.io.transform_write.pdf_transformer import (
    PDFTransformer,
    TransformerWriteContext,
)
from ptext.pdf.pdf import PDF
from test.base_test import BaseTest


class TestWritePDF(BaseTest):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("write")

    def test_single_document(self):
        self.input_file = self.input_dir / "0200.pdf"
        super().test_single_document()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        # attempt to store PDF
        doc = None
        with open(file, "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle)

        with open(out_file, "wb") as out_file_handle:
            wc = TransformerWriteContext(destination=out_file_handle, root_object=doc)
            PDFTransformer().transform(context=wc, object_to_transform=doc)
