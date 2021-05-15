import json
import logging
import unittest
from pathlib import Path

import typing

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../logs/test-read-info-dictionary.log", level=logging.DEBUG
)


class TestReadDocumentInfo(Test):
    """
    This test attempts to read the DocumentInfo for each PDF in the corpus
    """

    @unittest.skip
    def test_corpus(self):
        super(TestReadDocumentInfo, self).test_corpus()

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0068_page_0.pdf"))

    def _test_document(self, file) -> bool:
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            doc_info = doc.get_document_info()
            print("title    : %s" % doc_info.get_title())
            print("author   : %s" % doc_info.get_author())
            print("creator  : %s" % doc_info.get_creator())
            print("producer : %s" % doc_info.get_producer())
            print("ids      : %s" % doc_info.get_ids())
            print("language : %s" % doc_info.get_language())
            print("")
        return True

    def _count_errors(self) -> None:
        with open(
            "/home/joris/PycharmProjects/ptext/tests/output/testreaddocumentinfo.json",
            "r",
        ) as json_file_handle:
            test_data = json.loads(json_file_handle.read())
            exception_count: typing.Dict[str, int] = {}
            for e in [
                x["exception"] for x in test_data["per_document"] if not x["passed"]
            ]:
                exception_count[e] = exception_count.get(e, 0) + 1
            for k, v in exception_count.items():
                print("%d\t%s" % (v, k))


if __name__ == "__main__":
    TestReadDocumentInfo()._count_errors()
