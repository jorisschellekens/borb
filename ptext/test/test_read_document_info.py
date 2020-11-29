import unittest

from ptext.pdf import PDF
from ptext.test.base_test import BaseTest


class TestReadDocumentInfo(BaseTest):
    """
    This test attempts to read the DocumentInfo for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_single_document(self):
        self.input_file = self.input_dir / "document_897_single_page.pdf"
        super().test_single_document()

    def test_against_previous_fails(self):
        super().test_against_previous_fails()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):
        if "document_505_single_page" in str(file):
            return
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            doc_info = doc.get_document_info()
            print("title    : %s" % doc_info.get_title())
            print("author   : %s" % doc_info.get_author())
            print("creator  : %s" % doc_info.get_creator())
            print("producer : %s" % doc_info.get_producer())
            print("ids      : %s" % doc_info.get_ids())
            print("language : %s" % doc_info.get_language())


if __name__ == "__main__":
    unittest.main()
