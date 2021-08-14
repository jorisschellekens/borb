import typing
import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit.ocr.ocr_as_optional_content_group import OCRAsOptionalContentGroup
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractTextUsingOCR(unittest.TestCase):
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

    def test_write_ocr_as_optional_content_group(self):
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = OCRAsOptionalContentGroup(
                Path("/home/joris/Downloads/tessdata-master/")
            )
            doc = PDF.loads(pdf_file_handle, [l])
        with open(self.output_dir / "output_001.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

    def test_read_enhanced_document(self):

        # extract text from document
        l = SimpleTextExtraction()
        with open(self.output_dir / "output_001.pdf", "rb") as pdf_file_handle:
            PDF.loads(pdf_file_handle, [l])
        txt: str = l.get_text_for_page(0)

        # define ground truth
        ground_truth: str = """
        H2020 Programme
        AGA  – Annotated Model Grant Agreement
        Version 5.2
        26 June 2019
        Disclaimer
        This guide is aimed at assisting beneficiaries. It is provided for information purposes only and is not intended
        to replace consultation of any applicable legal sources. Neither the Commission nor the Executive Agencies (or
        any person acting on their behalf) can be held responsible for the use made of this guidance document.
        The EU Framework Programme
        for Research and Innovation
        HORIZON2020        
        """

        # compare the two
        # fmt: off
        letter_frequency_001: typing.Dict[str, int] = {x:sum([1 for c in ground_truth if c == x]) for x in "abcdefghijklmnopqrstuvwxyz"}
        letter_frequency_002: typing.Dict[str, int] = {x:sum([1 for c in txt if c == x]) for x in "abcdefghijklmnopqrstuvwxyz"}
        # fmt: on

        # assert
        assert all(
            [letter_frequency_002[k] == v for k, v in letter_frequency_001.items()]
        )


if __name__ == "__main__":
    unittest.main()
