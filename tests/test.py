import json
import multiprocessing
import os
import time
import typing
import unittest
from pathlib import Path


class TestResult:
    def __init__(
        self, file: Path, time: float, passed: bool, timed_out: bool, exception: str
    ):
        self.file: Path = file
        self.time = time
        self.passed = passed
        self.exception = exception
        self.timed_out = timed_out


class Test(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.maximum_test_time = 30
        self.input_dir = Path("/home/joris/Code/pdf-corpus/")
        self.test_results: typing.List[TestResult] = []

    def test_document(self, input_file: Path) -> bool:
        return False

    def test_corpus(self):
        pdf_file_names = os.listdir(self.input_dir)
        pdfs = [(self.input_dir / x) for x in pdf_file_names if x.endswith(".pdf")]
        self._test_list_of_documents(pdfs)

    def test_previous_fails(self):
        json_file = self._get_json_file()
        previous_fails = []
        try:
            with open(json_file, "r") as json_file_handle:
                previous_fails = [
                    self.input_dir / (x["file"] + ".pdf")
                    for x in json.loads(json_file_handle.read())["per_document"]
                    if not x["passed"]
                ]
        except:
            pass
        self._test_list_of_documents(previous_fails)

    def _test_list_of_documents(self, documents: typing.List[Path]):
        n = 0
        m = len(documents)
        for pdf_file in documents:
            print("Processing %s .. [%d / %d]" % (pdf_file, n, m))
            n += 1
            self.test_single_document_wrapper(pdf_file)

    def test_single_document_wrapper(self, input_file: Path):

        # start new thread to run test
        q = multiprocessing.Queue()
        process_a = multiprocessing.Process(
            target=self.test_single_document_in_thread_wrapper, args=(input_file, q)
        )
        process_a.start()

        # stop process if it hasn't stopped yet after timeout
        time_before = time.time()
        while (
            process_a.is_alive()
            and (time.time() - time_before) < self.maximum_test_time
        ):
            time.sleep(0.5)

        if process_a.is_alive():
            self.test_results.append(
                TestResult(input_file, self.maximum_test_time, False, True, None)
            )
            process_a.terminate()
        else:
            self.test_results.append(q.get())

        # call to processing method
        self.process_test_results()

    def test_single_document_in_thread_wrapper(
        self, input_file: Path, queue: multiprocessing.Queue
    ):
        before = time.time()
        try:
            val = self.test_document(input_file)
            delta = time.time() - before
            queue.put(
                TestResult(
                    input_file,
                    delta,
                    val,
                    False,
                    None,
                )
            )
        except BaseException as e:
            queue.put(
                TestResult(input_file, time.time() - before, False, False, str(e))
            )

    def _get_json_file(self):
        test_folder = Path(__file__)
        while test_folder.name != "tests":
            test_folder = test_folder.parent
        json_path = (
            test_folder / "results" / (self.__class__.__name__.lower() + ".json")
        )
        return json_path

    def get_test_results_as_json(self):
        if len(self.test_results) == 0:
            return
        d = [
            {
                "file": str(x.file.stem),
                "time_in_seconds": x.time,
                "passed": x.passed,
                "exception": str(x.exception),
                "timed_out": x.timed_out,
            }
            for x in self.test_results
        ]
        # raw count(s)
        passed_count = len([x for x in self.test_results if x.passed])
        failed_count = len([x for x in self.test_results if not x.passed])
        timed_out_count = len([x for x in self.test_results if x.timed_out])
        number_of_tests = len(self.test_results)

        # percentage(s)
        passed_percentage = passed_count / (number_of_tests + 0.0)
        failed_percentage = failed_count / (number_of_tests + 0.0)
        timed_out_percentage = timed_out_count / (number_of_tests + 0.0)

        # timing
        average_time_in_seconds = (
            0
            if passed_count == 0
            else sum([x.time for x in self.test_results if x.passed]) / passed_count
        )

        s = {
            "passed_count": passed_count,
            "passed_percentage": passed_percentage,
            "failed_count": failed_count,
            "failed_percentage": failed_percentage,
            "timed_out_count": timed_out_count,
            "timed_out_percentage": timed_out_percentage,
            "average_time_in_seconds": average_time_in_seconds,
            "count": number_of_tests,
        }

        return {"per_document": d, "summary": s}

    def process_test_results(self):
        with open(self._get_json_file(), "w") as json_file_handle:
            json_file_handle.write(
                json.dumps(self.get_test_results_as_json(), indent=4)
            )
