import datetime
import json
import os
import time
import unittest
from pathlib import Path


class BaseTest(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # accounting
        self.number_of_fails = 0
        self.number_of_passes = 0
        self.exceptions_per_document = {}
        self.time_per_document = {}
        # io
        self.input_dir = Path("/home/joris/Code/pdf-corpus/")
        self.input_file = self.input_dir / "document_1031_single_page.pdf"
        self.output_dir = Path("svg")

    def test_single_document(self):
        print("Processing %s .. [1 / 1]" % self.input_file)
        self._test_document(self.input_file)

    def test_against_entire_corpus(self):
        # attempt to read each file
        n = 0
        m = len(os.listdir(self.input_dir))
        for pdf_file in os.listdir(self.input_dir):
            if pdf_file in [
                "document_196_single_page.pdf",
                "document_1157.pdf",
                "document_442.pdf",
                "document_1151.pdf",
                "document_96.pdf",
            ]:
                continue
            if not pdf_file.endswith(".pdf"):
                continue
            # call test method for single document
            try:
                print("Processing %s .. [%d / %d]" % (pdf_file, n, m))
                n += 1
                elapsed = time.time()
                self._test_document(self.input_dir / pdf_file)
                elapsed = time.time() - elapsed
                self.number_of_passes += 1
                self.time_per_document[pdf_file] = int(elapsed * 10) / 10
            except Exception as e:
                self.number_of_fails += 1
                self.exceptions_per_document[pdf_file] = str(e)

            # persist results
            self.write_test_info()

    def _test_document(self, file):
        pass

    def write_test_info(self):

        if self.number_of_passes + self.number_of_fails == 0:
            return

        # time
        now = datetime.datetime.now()

        # inverse dict
        count_per_exception = {}
        for k, v in self.exceptions_per_document.items():
            if v not in count_per_exception:
                count_per_exception[v] = 1
            else:
                count_per_exception[v] += 1

        # persist
        with open(
            "%s_%d_%d_%d.json"
            % (self.__class__.__name__.lower(), now.day, now.month, now.year),
            "w",
        ) as json_file_handle:
            json_file_handle.write(
                json.dumps(
                    {
                        "time_per_document": self.time_per_document,
                        "exceptions_per_document": self.exceptions_per_document,
                        "count_per_exception": count_per_exception,
                        "totals": {
                            "number_of_documents": (
                                self.number_of_passes + self.number_of_fails
                            ),
                            "success": self.number_of_passes
                            / (self.number_of_passes + self.number_of_fails),
                            "fail": self.number_of_fails
                            / (self.number_of_passes + self.number_of_fails),
                        },
                    },
                    indent=3,
                )
            )
