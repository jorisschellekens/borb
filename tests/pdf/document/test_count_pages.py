import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF


class TestCountPages(unittest.TestCase):
    def test_count_pages(self):

        with open(Path("/home/joris/Code/pdf-corpus/0118.pdf"), "rb") as file_handle:
            doc = PDF.loads(file_handle)

            # check whether get_page and get_page_number return matching numbers
            page0 = doc.get_page(0)
            page_nr = page0.get_page_info().get_page_number()
            assert page_nr == 0

            # check number_of_pages
            assert doc.get_document_info().get_number_of_pages() == 2
