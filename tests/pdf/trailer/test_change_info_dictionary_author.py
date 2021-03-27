import logging
import unittest
from pathlib import Path

from ptext.io.read.types import String, Name, Dictionary
from ptext.pdf.pdf import PDF
from tests.test import Test
from tests.util import get_output_dir

logging.basicConfig(
    filename="../../logs/test-change-info-dictionary-author.log", level=logging.DEBUG
)


class TestChangeInfoDictionaryAuthor(Test):
    """
    This test attempts to read the DocumentInfo for each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-change-info-dictionary-author")

    @unittest.skip
    def test_corpus(self):
        super(TestChangeInfoDictionaryAuthor, self).test_corpus()

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def _test_document(self, file) -> bool:

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        doc = None
        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        if "XRef" not in doc:
            return False
        if "Trailer" not in doc["XRef"]:
            return False

        if "Info" not in doc["XRef"]["Trailer"]:
            doc["XRef"]["Trailer"][Name("Info")] = Dictionary()

        # change author
        doc["XRef"]["Trailer"]["Info"][Name("Author")] = String("Joris Schellekens")

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")
        with open(out_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        return True


if __name__ == "__main__":
    unittest.main()
