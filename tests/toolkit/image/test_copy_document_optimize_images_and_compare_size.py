import os
import random
import time
import typing
import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit import ImageFormatOptimization
from tests.test_case import TestCase


class TestCopyDocumentOptimizeImageAndCompareSize(TestCase):
    """
    This test opens every PDF from a corpus of PDF documents.
    """

    CORPUS_DIRECTORY: Path = Path("/home/joris/Code/pdf-corpus/")
    NUMBER_OF_DOCUMENTS: int = 0
    NUMBER_OF_FAILS: int = 0
    NUMBER_OF_PASSES: int = 0
    TIMING_INFORMATION: typing.Dict[str, float] = {}
    FILESIZE_INFORMATION: typing.Dict[str, float] = {}

    def test_open_10_documents(self):
        pdf_file_names = os.listdir(self.CORPUS_DIRECTORY)
        pdfs = [
            (self.CORPUS_DIRECTORY / x)
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
        pdf_file_names = os.listdir(self.CORPUS_DIRECTORY)
        pdfs = [
            (self.CORPUS_DIRECTORY / x)
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
        pdf_file_names = os.listdir(self.CORPUS_DIRECTORY)
        pdfs = [
            (self.CORPUS_DIRECTORY / x)
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
        self.TIMING_INFORMATION = {}
        self.NUMBER_OF_DOCUMENTS = 0
        self.NUMBER_OF_PASSES = 0
        self.NUMBER_OF_FAILS = 0
        self.FILESIZE_INFORMATION = {}
        for i, doc in enumerate(documents):
            try:
                print("processing %s [%d/%d] ..." % (doc.stem, i + 1, len(documents)))

                # read
                delta: float = time.time()
                file_size_0: int = os.path.getsize(doc)
                with open(doc, "rb") as pdf_file_handle:
                    pdf = PDF.loads(pdf_file_handle, [ImageFormatOptimization()])
                delta = time.time() - delta
                self.TIMING_INFORMATION[doc.stem] = delta

                # get file size
                with open(self.get_first_output_file(), "wb") as fh:
                    PDF.dumps(fh, pdf)
                file_size_1: int = os.path.getsize(self.get_first_output_file())
                self.get_first_output_file().unlink(missing_ok=True)
                self.FILESIZE_INFORMATION[doc.stem] = file_size_1 / file_size_0
                self.NUMBER_OF_PASSES += 1
            except Exception as e:
                print("ERROR, document %s, %s" % (doc.name, str(e)))
                self.NUMBER_OF_FAILS += 1
                pass

        # debug
        avg_time_per_document: float = sum(self.TIMING_INFORMATION.values()) / len(
            self.TIMING_INFORMATION
        )
        max_time_per_document: float = max(self.TIMING_INFORMATION.values())
        min_time_per_document: float = min(self.TIMING_INFORMATION.values())

        avg_ratio_per_document: float = sum(self.FILESIZE_INFORMATION.values()) / len(
            self.FILESIZE_INFORMATION
        )
        max_ratio_per_document: float = max(self.FILESIZE_INFORMATION.values())
        min_ratio_per_document: float = min(self.FILESIZE_INFORMATION.values())

        print("TestCopyDocumentOptimizeImageAndCompareSize: ")
        print("    count:")
        print("        number of documents      : %d" % self.NUMBER_OF_DOCUMENTS)
        print("        number of passes         : %d" % self.NUMBER_OF_PASSES)
        print("        number of fails          : %d" % self.NUMBER_OF_FAILS)
        print("    timing:")
        print("        min time (s) per document: %f" % min_time_per_document)
        print("        avg time (s) per document: %f" % avg_time_per_document)
        print("        max time (s) per document: %f" % max_time_per_document)
        print("    similarity:")
        print("        min ratio per document   : %f" % min_ratio_per_document)
        print("        avg ratio per document   : %f" % avg_ratio_per_document)
        print("        max ratio per document   : %f" % max_ratio_per_document)
