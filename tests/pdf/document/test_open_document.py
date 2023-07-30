import os
import random
import time
import typing
import unittest
from pathlib import Path

from borb.pdf.pdf import PDF


class TestOpenDocument(unittest.TestCase):
    """
    This test opens every PDF from a corpus of PDF documents.
    """

    CORPUS_DIRECTORY: Path = Path("/home/joris/Code/pdf-corpus/")
    NUMBER_OF_DOCUMENTS: int = 0
    NUMBER_OF_FAILS: int = 0
    NUMBER_OF_PASSES: int = 0
    TIMING_INFORMATION: typing.Dict[str, float] = {}

    def test_open_10_documents(self):
        TestOpenDocument.TIMING_INFORMATION = {}
        TestOpenDocument.NUMBER_OF_DOCUMENTS = 0
        TestOpenDocument.NUMBER_OF_PASSES = 0
        TestOpenDocument.NUMBER_OF_FAILS = 0
        pdf_file_names = os.listdir(TestOpenDocument.CORPUS_DIRECTORY)
        pdfs = [
            (TestOpenDocument.CORPUS_DIRECTORY / x)
            for x in pdf_file_names
            if x.endswith(".pdf")
            and "page_0" in x
            and (x not in ["0566_page_0.pdf", "0213.pdf"])
        ]
        random.shuffle(pdfs)
        pdfs = pdfs[0:10]
        self._test_list_of_documents(pdfs)

    @unittest.skip
    def test_open_100_documents(self):
        TestOpenDocument.TIMING_INFORMATION = {}
        TestOpenDocument.NUMBER_OF_DOCUMENTS = 0
        TestOpenDocument.NUMBER_OF_PASSES = 0
        TestOpenDocument.NUMBER_OF_FAILS = 0
        pdf_file_names = os.listdir(TestOpenDocument.CORPUS_DIRECTORY)
        pdfs = [
            (TestOpenDocument.CORPUS_DIRECTORY / x)
            for x in pdf_file_names
            if x.endswith(".pdf")
            and "page_0" in x
            and (x not in ["0566_page_0.pdf", "0213.pdf"])
        ]
        random.shuffle(pdfs)
        pdfs = pdfs[0:100]
        self._test_list_of_documents(pdfs)

    @unittest.skip
    def test_open_500_documents(self):
        TestOpenDocument.TIMING_INFORMATION = {}
        TestOpenDocument.NUMBER_OF_DOCUMENTS = 0
        TestOpenDocument.NUMBER_OF_PASSES = 0
        TestOpenDocument.NUMBER_OF_FAILS = 0
        pdf_file_names = os.listdir(TestOpenDocument.CORPUS_DIRECTORY)
        pdfs = [
            (TestOpenDocument.CORPUS_DIRECTORY / x)
            for x in pdf_file_names
            if x.endswith(".pdf")
            and "page_0" in x
            and (x not in ["0566_page_0.pdf", "0213.pdf"])
        ]
        random.shuffle(pdfs)
        pdfs = pdfs[0:500]
        self._test_list_of_documents(pdfs)

    def _test_list_of_documents(self, documents: typing.List[Path]):
        self.NUMBER_OF_DOCUMENTS = len(documents)
        for i, doc in enumerate(documents):
            try:
                print("processing %s [%d/%d] ..." % (doc.stem, i + 1, len(documents)))
                delta: float = time.time()
                with open(doc, "rb") as pdf_file_handle:
                    pdf = PDF.loads(pdf_file_handle)
                delta = time.time() - delta
                self.TIMING_INFORMATION[doc.stem] = delta
                self.NUMBER_OF_PASSES += 1
            except Exception as e:
                print("ERROR, document %s, %s" % (doc.name, str(e)))
                self.NUMBER_OF_FAILS += 1
                pass

        # debug
        avg_ms_per_document: float = sum(self.TIMING_INFORMATION.values()) / len(
            self.TIMING_INFORMATION
        )
        max_ms_per_document: float = max(self.TIMING_INFORMATION.values())
        min_ms_per_document: float = min(self.TIMING_INFORMATION.values())
        print("TestOpenDocument: ")
        print("    number of documents      : %d" % self.NUMBER_OF_DOCUMENTS)
        print("    number of passes         : %d" % self.NUMBER_OF_PASSES)
        print("    number of fails          : %d" % self.NUMBER_OF_FAILS)
        print("    min time (s) per document: %f" % min_ms_per_document)
        print("    avg time (s) per document: %f" % avg_ms_per_document)
        print("    max time (s) per document: %f" % max_ms_per_document)
