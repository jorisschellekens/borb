import pathlib
import typing
import unittest

from borb.pdf import Pipeline, PDF, Source, GetKeywordsByPagewiseTFIDF


class TestGetKeywordsByPagewiseTFIDFFromCorpus(unittest.TestCase):

    CORPUS_DIRECTORY: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus"
    )

    @staticmethod
    def get_keywords_from_corpus_pdf(n: int) -> typing.List[str]:
        pdf_path: pathlib.Path = (
            TestGetKeywordsByPagewiseTFIDFFromCorpus.CORPUS_DIRECTORY / f"{n:04d}.pdf"
        )
        print(pdf_path)

        # process
        keywords = Pipeline([Source(), GetKeywordsByPagewiseTFIDF(10)]).process(
            PDF.read(pdf_path)
        )

        # return
        return keywords

    def test_get_keywords_0001(self):
        kw = TestGetKeywordsByPagewiseTFIDFFromCorpus.get_keywords_from_corpus_pdf(1)
        assert all(
            [x in kw for x in ["security", "gas", "equipment", "america", "demand"]]
        )

    def test_get_keywords_0004(self):
        kw = TestGetKeywordsByPagewiseTFIDFFromCorpus.get_keywords_from_corpus_pdf(4)
        assert all(
            [x in kw for x in ["vendor", "payee", "accounts", "payable", "controllers"]]
        )

    def test_get_keywords_0009(self):
        kw = TestGetKeywordsByPagewiseTFIDFFromCorpus.get_keywords_from_corpus_pdf(9)
        assert all(
            [
                x in kw
                for x in ["bruisend", "chaudfontaine", "heverlee", "frietjes", "bru"]
            ]
        )
