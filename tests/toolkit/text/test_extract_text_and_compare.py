import os
import random
import time
import typing
import unittest
from pathlib import Path

from borb.pdf.pdf import PDF
from borb.toolkit import SimpleTextExtraction


class TestExtractTextAndCompare(unittest.TestCase):
    """
    This test opens every PDF from a corpus of PDF documents.
    """

    CORPUS_DIRECTORY: Path = Path("/home/joris/Code/pdf-corpus/")
    TEXT_SIMILARITY_INFORMATION: typing.Dict[str, float] = {}
    NUMBER_OF_DOCUMENTS: int = 0
    NUMBER_OF_FAILS: int = 0
    NUMBER_OF_PASSES: int = 0
    TIMING_INFORMATION: typing.Dict[str, float] = {}

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
        self.TIMING_INFORMATION = {}
        self.NUMBER_OF_DOCUMENTS = 0
        self.NUMBER_OF_PASSES = 0
        self.NUMBER_OF_FAILS = 0
        self.TEXT_SIMILARITY_INFORMATION = {}
        self.NUMBER_OF_DOCUMENTS = len(documents)
        for i, doc in enumerate(documents):
            try:
                print("processing %s [%d/%d] ..." % (doc.stem, i + 1, len(documents)))
                delta: float = time.time()
                l: SimpleTextExtraction = SimpleTextExtraction()
                with open(doc, "rb") as pdf_file_handle:
                    pdf = PDF.loads(pdf_file_handle, [l])
                page_0_text: str = l.get_text()[0]

                # update timing information
                delta = time.time() - delta
                self.TIMING_INFORMATION[doc.stem] = delta

                # read ground truth
                page_0_ground_truth: str = ""
                with open(doc.parent / (doc.stem + ".txt"), "r") as fh:
                    page_0_ground_truth = fh.read()

                # mark as PASS/FAIL
                similarity: float = TestExtractTextAndCompare._get_text_similarity(
                    page_0_text, page_0_ground_truth
                )
                self.TEXT_SIMILARITY_INFORMATION[doc.stem] = similarity
                if similarity > 0.99:
                    self.NUMBER_OF_PASSES += 1
                else:
                    self.NUMBER_OF_FAILS += 1

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

        avg_similarity_per_document: float = sum(
            self.TEXT_SIMILARITY_INFORMATION.values()
        ) / len(self.TEXT_SIMILARITY_INFORMATION)
        max_similarity_per_document: float = max(
            self.TEXT_SIMILARITY_INFORMATION.values()
        )
        min_similarity_per_document: float = min(
            self.TEXT_SIMILARITY_INFORMATION.values()
        )

        print("TestExtractTextAndCompare: ")
        print("    count:")
        print("        number of documents      : %d" % self.NUMBER_OF_DOCUMENTS)
        print("        number of passes         : %d" % self.NUMBER_OF_PASSES)
        print("        number of fails          : %d" % self.NUMBER_OF_FAILS)
        print("    timing:")
        print("        min time (s) per document: %f" % min_time_per_document)
        print("        avg time (s) per document: %f" % avg_time_per_document)
        print("        max time (s) per document: %f" % max_time_per_document)
        print("    similarity:")
        print("        min similarity per document: %f" % min_similarity_per_document)
        print("        avg similarity per document: %f" % avg_similarity_per_document)
        print("        max similarity per document: %f" % max_similarity_per_document)

    @staticmethod
    def _get_text_similarity(s0: str, s1: str) -> float:
        h0: typing.Dict[str, int] = {}
        h1: typing.Dict[str, int] = {}
        for c in s0:
            if c.isalnum():
                h0[c] = h0.get(c, 0) + 1
        for c in s1:
            if c.isalnum():
                h1[c] = h1.get(c, 0) + 1
        delta: float = 0
        for k in h0.keys():
            delta += abs(h0.get(k, 0) - h1.get(k, 0)) / max(h0.get(k, 0), h1.get(k, 0))
        return 1.0 - delta
