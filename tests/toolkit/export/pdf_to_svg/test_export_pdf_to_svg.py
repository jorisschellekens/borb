import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import typing

from borb.pdf import Document
from borb.pdf.pdf import PDF
from borb.toolkit.export.pdf_to_svg import PDFToSVG


class TestExportPDFToSVG(unittest.TestCase):
    """
    This test attempts to export each PDF in the corpus to SVG
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

    def test_convert_pdf_to_svg_as_eventlistener(self):
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = PDFToSVG()
            doc = PDF.loads(pdf_file_handle, [l])
            im = l.convert_to_svg()[0]
            with open(self.output_dir / "output_001.svg", "wb") as svg_file_handle:
                svg_file_handle.write(ET.tostring(im))

        return True

    def test_convert_pdf_to_svg_as_static_method(self):
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        doc: typing.Optional[Document] = None
        with open(input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # convert
        assert doc is not None
        im = PDFToSVG.convert_pdf_to_svg(doc)[0]

        # store
        with open(self.output_dir / "output_002.svg", "wb") as svg_file_handle:
            svg_file_handle.write(ET.tostring(im))


if __name__ == "__main__":
    unittest.main()
