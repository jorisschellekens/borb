import pathlib
import sys
import time
import typing
import unittest

from borb.pdf import PDF


class TestOpenCorpus(unittest.TestCase):

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
        "/home/joris-schellekens/Code/borb-pdf-corpus/pdf"
    )

    # @unittest.skip
    def test_open_corpus(self):
        positive: typing.List[pathlib.Path] = []
        positive_timing: typing.List[float] = []
        negative: typing.List[pathlib.Path] = []
        negative_timing: typing.List[float] = []
        reasons_for_failure: typing.Dict[str, int] = {}
        M: typing.List[pathlib.Path] = [
            x
            for x in TestOpenCorpus.CORPUS_DIRECTORY.iterdir()
            if x.name.endswith(".pdf")
        ]
        M = sorted(M, key=lambda x: x.name)
        N: int = len(M)
        for i, pdf_file in enumerate(M):
            # fmt: off
            if pdf_file.name in [
                "0010.pdf", "0026.pdf", "0041.pdf", "0069.pdf", "0074.pdf",
                "0076.pdf", "0079.pdf", "0080.pdf", "0081.pdf", "0083.pdf",
                "0084.pdf", "0085.pdf", "0095.pdf", "0119.pdf", "0123.pdf",
                "0167.pdf", "0176.pdf", "0182.pdf", "0194.pdf", "0201.pdf",
                "0203.pdf", "0217.pdf", "0226.pdf", "0232.pdf", "0237.pdf",
                "0245.pdf", "0254.pdf", "0272.pdf", "0278.pdf", "0280.pdf",
                "0281.pdf", "0287.pdf", "0288.pdf", "0297.pdf", "0314.pdf",
                "0319.pdf", "0333.pdf", "0341.pdf", "0380.pdf", "0395.pdf",
                "0416.pdf", "0422.pdf", "0427.pdf", "0429.pdf", "0431.pdf",
                "0470.pdf", "0482.pdf", "0483.pdf", "0498.pdf", "0505.pdf",
                "0508.pdf", "0546.pdf", "0560.pdf", "0564.pdf", "0568.pdf",
                "0569.pdf", "0589.pdf", "0590.pdf", "0592.pdf", "0610.pdf",
                "0620.pdf", "0621.pdf", "0626.pdf"
            ]:
                continue
            # fmt: on
            if not pdf_file.name.endswith(".pdf"):
                continue

            # debug
            print(
                f"[{i} {N} {round(i / N, 2)}, {len(positive)} {round(len(positive_timing) / i, 2) if i != 0 else 0}] Attempting to read {pdf_file}"
            )

            # try opening
            before: float = time.time()
            try:
                PDF.read(where_from=pdf_file)
                positive_timing += [time.time() - before]
                positive += [pdf_file]
            except Exception as e:
                print(f"Unable to read {pdf_file}")
                reasons_for_failure[str(e)] = reasons_for_failure.get(str(e), 0) + 1
                negative_timing += [time.time() - before]
                negative += [pdf_file]

        # debug
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

        # print all reasons
        if len(reasons_for_failure) > 0:
            print("\treasons:")
            for k, v in reasons_for_failure.items():
                print(f"\t\t- {k}: {round(v/sum(reasons_for_failure.values()), 2)}")

        # print all negative
        if len(negative) > 0:
            print("\tfiles:")
            for pdf_file in negative:
                print(f"\t\t- {pdf_file}")

    # @unittest.skip
    def test_open_single_file_from_corpus(self):
        d = PDF.read(where_from=TestOpenCorpus.CORPUS_DIRECTORY / "0007.pdf")
