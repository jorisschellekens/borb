import unittest

from ptext.pdf.pdf import PDF
from test.base_test import BaseTest


class TestReadDocumentInfo(BaseTest):
    """
    This test attempts to read the DocumentInfo for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_single_document(self):
        self.input_file = self.input_dir / "0134_page_0.pdf"
        super().test_single_document()

    def test_against_previous_fails(self):
        super().test_against_previous_fails()

    def test_against_entire_corpus(self):
        super().test_against_entire_corpus()

    def _test_document(self, file):
        if "0287" in file.stem:
            return
        if "0190" in file.stem:
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
