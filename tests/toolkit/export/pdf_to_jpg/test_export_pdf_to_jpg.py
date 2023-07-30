import typing
import unittest
from pathlib import Path

from borb.pdf import Document
from borb.pdf.pdf import PDF
from borb.toolkit.export.pdf_to_jpg import PDFToJPG
from tests.test_case import TestCase


class TestExportPDFToJPG(TestCase):
    """
    This test attempts to export each PDF in the corpus to SVG
    """

    def test_convert_pdf_to_jpg_as_eventlistener(self):
        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = PDFToJPG()
            doc = PDF.loads(pdf_file_handle, [l])
            im = l.convert_to_jpg()[0]
            im.save(self.get_artifacts_directory() / "output_001.jpg")
        return True

    def test_convert_pdf_to_jpg_as_static_method(self):
        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        doc: typing.Optional[Document] = None
        with open(input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        assert doc is not None
        PDFToJPG.convert_pdf_to_jpg(doc)[0].save(
            self.get_artifacts_directory() / "output_002.jpg"
        )


if __name__ == "__main__":
    unittest.main()
