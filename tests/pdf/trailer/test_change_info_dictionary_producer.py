import logging
import unittest
from pathlib import Path

from ptext.io.read.types import String, Name, Dictionary
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../../logs/test-change-info-dictionary-producer.log", level=logging.DEBUG
)


class TestChangeInfoDictionaryProducer(Test):
    """
    This test attempts to read the DocumentInfo for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../output/test-change-info-dictionary-producer")

    def test_corpus(self):
        super(TestChangeInfoDictionaryProducer, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_document(self, file) -> bool:

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        doc = None
        with open(file, "rb") as pdf_file_handle:
            doc = None
            with open(file, "rb") as pdf_file_handle:
                doc = PDF.loads(pdf_file_handle)

        if "XRef" not in doc:
            return False
        if "Trailer" not in doc["XRef"]:
            return False

        if "Info" not in doc["XRef"]["Trailer"]:
            doc["XRef"]["Trailer"][Name("Info")] = Dictionary()

        # change producer
        doc["XRef"]["Trailer"]["Info"]["Producer"] = String("pText")

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        return True


if __name__ == "__main__":
    unittest.main()
