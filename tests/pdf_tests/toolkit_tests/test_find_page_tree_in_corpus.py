import pathlib
import re
import time
import typing
import unittest

from borb.pdf import PDF, Document, Page
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_events_as_json import GetEventsAsJSON
from borb.pdf.toolkit.sink.get_text import GetText
from borb.pdf.toolkit.source.operator.source import Source


class TestFindPageTreeInCorpus(unittest.TestCase):

    # Path to the directory containing a collection of PDF documents used for testing.
    #
    # Users must adjust this path to match the location of the PDF corpus on their system
    # to run the tests successfully. A large collection of PDF documents is available
    # on the author's GitHub repository, which can be cloned or downloaded to use as the
    # test corpus.
    #
    # Ensure that the directory specified by this path exists and contains the necessary
    # PDF files before running the tests.
    CORPUS_DIRECTORY: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus"
    )

    # @unittest.skip
    def test_read_corpus(self):
        for pdf_file in TestFindPageTreeInCorpus.CORPUS_DIRECTORY.iterdir():

            if not pdf_file.name.endswith(".pdf"):
                continue
            if pdf_file.name in [
                "0365_page_0.pdf",
                "0390_page_0.pdf",
                "0457_page_0.pdf",
                "0364_page_0.pdf",
                "0565_page_0.pdf",
                "0539_page_0.pdf",  # bracket balancing in source.py
                "0240_page_0.pdf",  # bracket balancing in source.py
                "0487_page_0.pdf",  # infinite loop?
                "0458_page_0.pdf",  # infinite loop?
                "0465_page_0.pdf",  # infinite loop?
                "0407_page_0.pdf",  # infinite loop?
                "0218_page_0.pdf",
                "0275_page_0.pdf",
                "0237_page_0.pdf",
                "0051_page_0.pdf",
                "0191_page_0.pdf",
                "0332_page_0.pdf",
            ]:
                continue

            # read
            try:
                doc = PDF.read(where_from=pdf_file)
                pages = doc["Trailer"]["Root"]["Pages"]["Kids"]
                is_tree = not all([isinstance(x, Page) for x in pages])
                if is_tree:
                    print(pdf_file)
            except:
                pass

            # pathlib.Path('/home/joris-schellekens/Code/borb-pdf-corpus/0176.pdf')

    def test_read_single_file(self):
        doc = PDF.read(TestFindPageTreeInCorpus.CORPUS_DIRECTORY / "0176.pdf")
        doc.insert_page(Page(), 5)
        doc.pop_page(5)
        PDF.write(what=doc, where_to="assets/output.pdf")
