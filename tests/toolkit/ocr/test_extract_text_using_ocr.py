import typing
import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestExtractTextUsingOCR(TestCase):
    @unittest.skip
    def test_write_ocr_as_optional_content_group(self):
        from borb.toolkit.ocr.ocr_as_optional_content_group import (
            OCRAsOptionalContentGroup,
        )

        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        tesseract_data_dir: Path = Path.home() / Path("Downloads/tessdata-main/")
        with open(input_file, "rb") as pdf_file_handle:
            l = OCRAsOptionalContentGroup(tesseract_data_dir)
            doc = PDF.loads(pdf_file_handle, [l])
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

    @unittest.skip
    def test_read_enhanced_document(self):

        # extract text from document
        l = SimpleTextExtraction()
        with open(self.get_first_output_file(), "rb") as pdf_file_handle:
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
