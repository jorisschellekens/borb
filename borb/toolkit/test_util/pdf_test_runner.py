#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A test runner is a component which orchestrates the execution of tests and provides the outcome to the user.
The runner may use a graphical interface, a textual interface,
or return a special value to indicate the results of executing the tests.

This class provides a convenience method to add a hook to the unittest framework.
This hook will ensure the output of the tests is exported to PDF.
"""
import datetime
import logging
import subprocess
import time
import typing
import unittest
from pathlib import Path

from borb.pdf.document.document import Document
from borb.pdf.pdf import PDF
from borb.toolkit.test_util.default_test_renderer import DefaultTestRenderer
from borb.toolkit.test_util.test_info import TestResult
from borb.toolkit.test_util.test_renderer import TestRenderer
from borb.toolkit.test_util.test_status import TestStatus

logger = logging.getLogger(__name__)


class PDFTestRunner:
    """
    A test runner is a component which orchestrates the execution of tests and provides the outcome to the user.
    The runner may use a graphical interface, a textual interface,
    or return a special value to indicate the results of executing the tests.

    This class provides a convenience method to add a hook to the unittest framework.
    This hook will ensure the output of the tests is exported to PDF.
    """

    # keep track of all statuses
    _is_initialized: bool = False
    _test_id_to_start_time: typing.Dict[int, float] = {}
    _test_statuses: typing.List["TestResult"] = []

    #
    # PRIVATE
    #

    @staticmethod
    def _add_test_info(test_case: unittest.TestCase, status: TestStatus) -> None:
        test_case_started_at: float = min(PDFTestRunner._test_id_to_start_time.values())
        if id(test_case) in PDFTestRunner._test_id_to_start_time:
            test_case_started_at = PDFTestRunner._test_id_to_start_time[id(test_case)]
        # noinspection PyProtectedMember
        PDFTestRunner._test_statuses.append(
            TestResult(
                file=test_case.__module__,
                method=test_case._testMethodName,
                class_name=test_case.__class__.__name__,
                started_at=test_case_started_at,
                status=status,
                stopped_at=time.time(),
            )
        )

    @staticmethod
    def _build_pdf(
        renderer: TestRenderer,
        report_name: Path,
        open_when_finished: bool,
    ) -> None:
        # sort tests
        PDFTestRunner._test_statuses.sort(
            key=lambda x: x.get_file() + "/" + x.get_class_name() + "/" + x.get_method()
        )

        # create empty Document
        logger.debug("creating empty Document")
        doc: Document = Document()

        # (front) cover page
        logger.debug("adding (front) cover page(s) to Document")
        renderer.build_pdf_front_cover_page(doc)

        # summary
        logger.debug("adding summary Page(s) to Document")
        renderer.build_pdf_summary_page(doc, PDFTestRunner._test_statuses)

        # class level results
        file_name_sorted: typing.List[str] = sorted(
            [x for x in set([x.get_file() for x in PDFTestRunner._test_statuses])]
        )
        for i, class_name in enumerate(file_name_sorted):
            logger.debug(
                "building class level results %d/%d" % (i + 1, len(file_name_sorted))
            )
            renderer.build_pdf_module_page(
                doc,
                [x for x in PDFTestRunner._test_statuses if x.get_file() == class_name],
            )

        # (back) cover page
        logger.debug("adding (back) cover page(s) to Document")
        renderer.build_pdf_back_cover_page(doc)

        # write PDF
        logger.debug("writing PDF to file")
        with open(report_name, "wb") as fh:
            PDF.dumps(fh, doc)

        # open
        if open_when_finished:
            logger.debug("opening PDF")
            subprocess.call(("xdg-open", report_name))

    #
    # PUBLIC
    #

    @staticmethod
    def set_up(
        test_case: unittest.TestCase,
        report_name: Path = Path(
            "Test Report %s.pdf" % datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ),
    ):
        """
        This function sinks its hooks into the unittest framework and ensures
        every test (result) is captured and its results can be output to PDF.
        :param test_case:       the unittest.TestCase that provides the entrypoint into the unittest code
        :param report_name:     the Path determining where to write the output PDF
        :return:            None
        """

        # find TestResult
        # we will modify its methods to add our hook(s)
        test_result: typing.Optional[unittest.TestResult] = None
        try:
            # noinspection PyProtectedMember
            test_result = test_case._outcome.result
        except:
            pass
        if test_result is None:
            return

        # prevent ourselves from adding the hook(s) twice
        if PDFTestRunner._is_initialized:
            return
        PDFTestRunner._is_initialized = True

        # addError
        # fmt: on
        prev_add_error = test_result.addError

        def new_add_error(t: unittest.TestCase, err: typing.Any):
            """
            Called when an error has occurred. 'err' is a tuple of values as
            returned by sys.exc_info().
            :param t:
            :param err:
            :return:
            """
            PDFTestRunner._add_test_info(t, TestStatus.ERROR)
            prev_add_error(t, err)

        test_result.addError = new_add_error
        # fmt: on

        # addExpectedFailure
        # fmt: off
        prev_add_expected_failure = test_result.addExpectedFailure
        def new_add_expected_failure(t: unittest.TestCase, err: str):
            """
            Called when an expected failure/error occurred."
            :param t:
            :param err:
            :return:
            """
            PDFTestRunner._add_test_info(t, TestStatus.EXPECTED_FAILURE)
            prev_add_expected_failure(t, err)
        test_result.addExpectedFailure = new_add_expected_failure
        # fmt: on


        # addFailure
        # fmt: off
        prev_add_failure = test_result.addFailure
        def new_add_failure(t: unittest.TestCase, err: typing.Any):
            """
            Called when an error has occurred. 'err' is a tuple of values as
            returned by sys.exc_info().
            :param t:
            :param err:
            :return:
            """
            PDFTestRunner._add_test_info(t, TestStatus.FAILURE)
            prev_add_failure(t, err)
        test_result.addFailure = new_add_failure
        # fmt: on

        # addSkip
        # fmt: off
        prev_add_skip = test_result.addSkip
        def new_add_skip(t: unittest.TestCase, r: str):
            """
            Called when a test is skipped.
            :param t:
            :param r:
            :return:
            """
            PDFTestRunner._add_test_info(t, TestStatus.SKIP)
            prev_add_skip(t, r)
        test_result.addSkip = new_add_skip
        # fmt: on

        # addSuccess
        # fmt: off
        prev_add_success = test_result.addSuccess
        def new_add_success(t: unittest.TestCase):
            """
            Called when a test has completed successfully
            :param t:
            :return:
            """
            PDFTestRunner._add_test_info(t, TestStatus.SUCCESS)
            prev_add_success(t)
        test_result.addSuccess = new_add_success
        # fmt: on

        # addUnexpectedSuccess
        # fmt: off
        prev_add_unexpected_success = test_result.addUnexpectedSuccess
        def new_add_unexpected_success(t: unittest.TestCase):
            """
            Called when a test was expected to fail, but succeed.
            :param t:
            :return:
            """
            PDFTestRunner._add_test_info(t, TestStatus.UNEXPECTED_SUCCESS)
            prev_add_unexpected_success(t)
        test_result.addUnexpectedSuccess = new_add_unexpected_success
        # fmt: on

        # startTest
        # fmt: off
        prev_start_test = test_result.startTest
        def new_start_test(t: unittest.TestCase):
            """
            Called when the given test is about to be run
            :param t:
            :return:
            """
            PDFTestRunner._test_id_to_start_time[id(t)] = time.time()
            prev_start_test(t)
        test_result.startTest = new_start_test
        # fmt: on

        # startTestRun
        # fmt: off
        prev_start_test_run = test_result.startTestRun
        def new_start_test_run():
            """
            Called once before any tests are executed.
            See startTest for a method called before each test.
            :return:
            """
            PDFTestRunner._test_id_to_start_time.clear()
            PDFTestRunner._test_statuses.clear()
            PDFTestRunner._test_id_to_start_time[-1] = time.time()
            prev_start_test_run()
        test_result.startTestRun = new_start_test_run
        # fmt: on

        # stopTestRun
        # fmt: off
        prev_stop_test_run = test_result.stopTestRun
        def new_stop_test_run():
            """
            Called once after all tests are executed.
            See stopTest for a method called after each test.
            :return:
            """
            prev_stop_test_run()
            PDFTestRunner._build_pdf(renderer=DefaultTestRenderer(),
                                     report_name=report_name,
                                     open_when_finished=True)
        test_result.stopTestRun = new_stop_test_run
        # fmt: on

        # add the earliest start of testing
        PDFTestRunner._test_id_to_start_time[-1] = time.time()
