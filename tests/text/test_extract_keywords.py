import json
import logging
import unittest
from pathlib import Path

from ptext.toolkit.text.stop_words import ENGLISH_STOP_WORDS
from ptext.toolkit.text.tf_idf_keyword_extraction import (
    TFIDFKeywordExtraction,
)
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../text/test-extract-keywords.log", level=logging.DEBUG)


class TestExtractKeywords(Test):
    """
    This test attempts to extract the keywords (TF-IDF)
    from each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../text/test-extract-keywords")

    def test_corpus(self):
        super(TestExtractKeywords, self).test_corpus()

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = TFIDFKeywordExtraction(ENGLISH_STOP_WORDS)
            doc = PDF.loads(pdf_file_handle, [l])

            # export txt
            output_file = self.output_dir / (file.stem + ".json")
            with open(output_file, "w") as json_file_handle:
                json_file_handle.write(
                    json.dumps(
                        [x.__dict__ for x in l.get_keywords_per_page(0, 5)], indent=4
                    )
                )

        return True


if __name__ == "__main__":
    unittest.main()
