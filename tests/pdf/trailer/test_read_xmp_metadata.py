import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../logs/test-read-xmp-meta-data.log", level=logging.DEBUG
)


class TestReadXMPMetaData(Test):
    """
    This test attempts to read the XMPDocumentInfo for each PDF in the corpus
    """

    def test_corpus(self):
        super(TestReadXMPMetaData, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0066.pdf"))

    def test_document(self, file) -> bool:
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            doc_info = doc.get_xmp_document_info()
            print("title                : %s" % doc_info.get_title())
            print("author               : %s" % doc_info.get_author())
            print("creator              : %s" % doc_info.get_creator())
            print("producer             : %s" % doc_info.get_producer())
            print("ids                  : %s" % doc_info.get_ids())
            print("language             : %s" % doc_info.get_language())
            print("document-ID          : %s" % doc_info.get_document_id())
            print("original document-ID : %s" % doc_info.get_original_document_id())
            print("creation date        : %s" % doc_info.get_creation_date())
            print("modification date    : %s" % doc_info.get_modification_date())
            print("metadata date        : %s" % doc_info.get_metadata_date())
            print("")
        return True


if __name__ == "__main__":
    unittest.main()
