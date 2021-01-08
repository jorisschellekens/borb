import logging

from ptext.io.read_transform.types import Dictionary
from ptext.pdf.pdf import PDF

from tests.test import Test

logging.basicConfig(
    filename="../annotations/test-extract-annotations.log", level=logging.DEBUG
)


class TestExtractAnnotations(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_corpus(self):
        super(TestExtractAnnotations, self).test_corpus()

    def test_document(self, file):
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            root = doc["XRef"]["Trailer"]["Root"]
            assert root is not None
            assert isinstance(root, Dictionary)
            if "Annotations" in root:
                print("%s has annotations")
        return True
