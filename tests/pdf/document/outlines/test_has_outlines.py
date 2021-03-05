import json
import logging
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../../../logs/test-has-outlines.log", level=logging.DEBUG)


class TestHasOutlines(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../../../output/test-has-outlines")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0121_page_0.pdf"))

    def test_corpus(self):
        super(TestHasOutlines, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / ("test_has_outlines.json")

        # attempt to read PDF
        doc = None
        has_outlines = False
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)
            has_outlines = doc.has_outlines()

        # read
        outline_json = {}
        try:
            with open(out_file, "r") as json_file_handle:
                json.loads(json_file_handle.read())
        except:
            pass

        print(file.stem + " : " + str(has_outlines))

        # update
        outline_json[file.stem] = has_outlines

        # write
        with open(out_file, "w") as json_file_handle:
            json_file_handle.write(json.dumps(outline_json, indent=4))

        return True
