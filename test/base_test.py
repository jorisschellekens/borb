import datetime
import json
import os
import time
import unittest
from pathlib import Path


class BaseTest(unittest.TestCase):
    """
    Base class for all TestCase objects that
    want to run against the entire corpus, or parts thereof.
    This class provides convenience methods for running
    against the entire corpus, previous fails, as well as logging.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # accounting
        self.number_of_fails = 0
        self.number_of_passes = 0
        self.exceptions_per_document = {}
        self.time_per_document = {}
        # io
        self.input_dir = Path("/home/joris/Code/pdf-corpus/")
        #self.input_dir = Path("/home/joris/PycharmProjects/pdf-corpus/")
        self.input_file = self.input_dir / "0004.pdf"
        self.output_dir = Path("svg")

    def test_single_document(self):
        print("Processing %s .. [1 / 1]" % self.input_file)
        self._test_document(self.input_file)

    def test_against_previous_fails(self):

        # json name
        json_name = "".join(
            [
                (c.lower() if c.lower() == c else "_" + c.lower())
                for c in self.__class__.__name__
            ]
        )[1:]

        # find latest test results
        last_known_date = None
        last_known_test_file = None
        for f in [
            f
            for f in os.listdir(Path(__file__).parent)
            if f.startswith(json_name) and f.endswith(".json")
        ]:
            date_parts = [int(x) for x in f[len(json_name) + 1 : -5].split("_")]
            date = datetime.datetime(date_parts[2], date_parts[1], date_parts[0])
            if last_known_date is None or date > last_known_date:
                last_known_date = date
                last_known_test_file = f

        # read test_results
        test_data = None
        with open(last_known_test_file, "r") as json_file_handle:
            test_data = json.loads(json_file_handle.read())

        # extract failed documents
        failed_documents = [k for k, v in test_data["exceptions_per_document"].items()]

        # attempt to read each file
        n = 0
        m = len(failed_documents)
        for pdf_file in failed_documents:

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
            self._write_test_info()

    def test_against_entire_corpus(self):
        # attempt to read each file
        n = 0
        m = len(os.listdir(self.input_dir))
        for pdf_file in os.listdir(self.input_dir):
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
            self._write_test_info()

    def _test_document(self, file):
        pass

    def _test_info_as_json(self):

        # inverse dict
        count_per_exception = {}
        for k, v in self.exceptions_per_document.items():
            if v not in count_per_exception:
                count_per_exception[v] = 1
            else:
                count_per_exception[v] += 1

        return {
            "time_per_document": self.time_per_document,
            "exceptions_per_document": self.exceptions_per_document,
            "count_per_exception": count_per_exception,
            "totals": {
                "number_of_documents": (self.number_of_passes + self.number_of_fails),
                "success": self.number_of_passes
                / (self.number_of_passes + self.number_of_fails),
                "fail": self.number_of_fails
                / (self.number_of_passes + self.number_of_fails),
            },
        }

    def _write_test_info(self):

        if self.number_of_passes + self.number_of_fails == 0:
            return

        # time
        now = datetime.datetime.now()

        # json name
        json_name = "".join(
            [
                (c.lower() if c.lower() == c else "_" + c.lower())
                for c in self.__class__.__name__
            ]
        )[1:]

        # persist
        with open(
            "%s_%d_%d_%d.json" % (json_name, now.day, now.month, now.year),
            "w",
        ) as json_file_handle:
            json_file_handle.write(
                json.dumps(
                    self._test_info_as_json(),
                    indent=3,
                )
            )
