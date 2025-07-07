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
        "/home/joris-schellekens/Code/borb-pdf-corpus"
    )

    #@unittest.skip
    def test_open_corpus(self):
        positive: typing.List[pathlib.Path] = []
        positive_timing: typing.List[float] = []
        negative: typing.List[pathlib.Path] = []
        negative_timing: typing.List[float] = []
        reasons_for_failure: typing.Dict[str, int] = {}
        M: typing.List[pathlib.Path] = [x for x in TestOpenCorpus.CORPUS_DIRECTORY.iterdir() if x.name.endswith('.pdf')]
        M = sorted(M, key=lambda x: x.name)
        N: int = len(M)
        for i, pdf_file in enumerate(M):
            if pdf_file.name in ['0000.pdf', '0002.pdf', '0006.pdf', '0013.pdf', '0048.pdf',
                                 '0089.pdf', '0101.pdf', '0105.pdf', '0109.pdf', '0121.pdf',
                                 '0139.pdf', '0173.pdf', '0180.pdf', '0190.pdf', '0196.pdf',
                                 '0225.pdf', '0248.pdf', '0249.pdf', '0250.pdf', '0254.pdf',
                                 '0272.pdf', '0273.pdf', '0311.pdf', '0320.pdf', '0345.pdf', '0373.pdf',
                                 '0381.pdf', '0425.pdf', '0430.pdf', '0432.pdf', '0436.pdf',
                                 '0466.pdf', '0468.pdf', '0477.pdf', '0483.pdf', '0495.pdf',
                                 '0500.pdf', '0551.pdf', '0560.pdf', '0563.pdf', '0565.pdf',
                                 '0567.pdf', '0568.pdf', '0578.pdf', '0579.pdf', '0583.pdf']:
                continue
            if not pdf_file.name.endswith(".pdf"):
                continue

            # debug
            print(f"[{i} {N} {round(i / N, 2)}, {len(positive)} {round(len(positive_timing) / i, 2) if i != 0 else 0}] Attempting to read {pdf_file}")

            # try opening
            before: float = time.time()
            try:
                PDF.read(where_from=pdf_file)
                positive_timing += [time.time() - before]
                positive += [pdf_file]
            except Exception as e:
                print(f'Unable to read {pdf_file}')
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

    #@unittest.skip
    def test_open_single_file_from_corpus(self):
        d = PDF.read(where_from=TestOpenCorpus.CORPUS_DIRECTORY / "0135.pdf")
