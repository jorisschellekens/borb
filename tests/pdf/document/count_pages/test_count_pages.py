import unittest
from pathlib import Path

from borb.pdf.pdf import PDF


class TestCountPages(unittest.TestCase):
    def test_get_page_number(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as file_handle:
            doc = PDF.loads(file_handle)

            # check whether get_page and get_page_number return matching numbers
            N: int = int(doc.get_document_info().get_number_of_pages())
            for i in range(0, N):
                page_object = doc.get_page(i)
                page_nr = page_object.get_page_info().get_page_number()
                assert page_nr == i

    def test_get_number_of_pages(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as file_handle:
            doc = PDF.loads(file_handle)
            assert doc.get_document_info().get_number_of_pages() == 2
