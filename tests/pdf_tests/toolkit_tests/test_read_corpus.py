import pathlib
import re
import time
import typing
import unittest

from borb.pdf import PDF, Document
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_text import GetText
from borb.pdf.toolkit.source.operator.source import Source


class TestReadCorpus(unittest.TestCase):

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
        positive: typing.List[pathlib.Path] = []
        positive_timing: typing.List[float] = []
        negative: typing.List[pathlib.Path] = []
        negative_timing: typing.List[float] = []
        error_buckets: typing.Dict[int, int] = {x: 0 for x in range(0, 110, 10)}
        for pdf_file in TestReadCorpus.CORPUS_DIRECTORY.iterdir():
            if not pdf_file.name.endswith(".pdf"):
                continue
            if not pdf_file.name.endswith("_page_0.pdf"):
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

            # try opening
            before: float = time.time()
            try:
                print(f"Attempting to read {pdf_file}")
                d: Document = PDF.read(where_from=pdf_file)
                positive_timing += [time.time() - before]
                positive += [pdf_file]

                txt0: str = (
                    Pipeline([Source(), GetText()]).process(d.get_page(0)).get(0, "")
                )
                txt1: str = ""
                with open(
                    TestReadCorpus.CORPUS_DIRECTORY
                    / (pdf_file.name.replace(".pdf", ".txt"))
                ) as fh:
                    txt1 = fh.read()
                txt0_trimmed = re.sub("[^a-zA-Z0-9]+", "", txt0)
                txt1_trimmed = re.sub("[^a-zA-Z0-9]+", "", txt1)
                l0 = len(txt0_trimmed)
                l1 = len(txt1_trimmed)
                error: int = 0
                if max(l0, l1) > 0:
                    error = abs(l0 - l1) / max(l0, l1)
                    error = int(error * 100)
                    error_down = error - (error % 10)
                    error_up = min(error_down + 10, 100)
                    if abs(error - error_down) < abs(error - error_up):
                        error = error_down
                    else:
                        error = error_up
                error_buckets[error] += 1
                print(
                    f"name: {pdf_file.name}, len0: {len(txt0_trimmed)}, len1:  {len(txt1_trimmed)}, err: {error}"
                )

            except Exception as e:
                negative_timing += [time.time() - before]
                negative += [pdf_file]

            if len(positive) + len(negative) >= 200:
                break

        # debug
        # fmt: off
        n: int = sum(error_buckets.values())
        print("ERROR:")
        for k,v in error_buckets.items():
            print(f"\t{k}: {round(v/n, 2)*100}")
        print('\n')
        # fmt: on

        # fmt: off
        n: int = len(positive) + len(negative)
        print("POSITIVE:")
        print(f"\tcount: {len(positive)}")
        print(f"\t    %: {round(len(positive)/n, 2)}")
        print(f"\t  duration (avg): {round(sum(positive_timing) / len(positive_timing), 2)}")
        print(f"\t           (max): {round(max(positive_timing), 2)}")
        print(f"\t           (min): {round(min(positive_timing), 2)}")
        # fmt: on

        # fmt: off
        print("NEGATIVE:")
        print(f"\tcount: {len(negative)}")
        print(f"\t    %: {round(len(negative)/n, 2)}")
        print(f"\t  duration (avg): {round(sum(negative_timing) / len(negative_timing), 2)}")
        print(f"\t           (max): {round(max(negative_timing), 2)}")
        print(f"\t           (min): {round(min(negative_timing), 2)}")
        # fmt: on

        # print all negative
        if len(negative) > 0:
            print("\tfiles:")
            for pdf_file in negative:
                print(f"\t\t- {pdf_file}")

    # @unittest.skip
    def test_read_single_pdf(self):
        d: Document = PDF.read(where_from=TestReadCorpus.CORPUS_DIRECTORY / "0002.pdf")

        while d.get_number_of_pages() > 1:
            d.pop_page(1)
        txt: str = Pipeline([Source(), GetText()]).process(d)[0]
