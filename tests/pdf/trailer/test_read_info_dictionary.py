import logging
import unittest
from pathlib import Path

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
        self._test_document(Path("/home/joris/Code/pdf-corpus/0105.pdf"))

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


if __name__ == "__main__":
    unittest.main()
