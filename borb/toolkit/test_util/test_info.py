#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class represents a result from the testsuite.
"""
from borb.toolkit.test_util.test_status import TestStatus


class TestResult:
    """
    This class represents a result from the testsuite.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        file: str,
        method: str,
        class_name: str,
        started_at: float,
        status: TestStatus,
        stopped_at: float,
    ):
        self._file: str = file
        self._method: str = method
        self._class_name: str = class_name
        self._started_at: float = started_at
        self._status: TestStatus = status
        self._stopped_at: float = stopped_at

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_class_name(self) -> str:
        """
        This function returns the class that defined the test
        :return:    the class that defined the test
        """
        return self._class_name

    def get_duration(self) -> int:
        """
        This function returns the duration of the test
        :return:    the duration of the test
        """
        return int(self._stopped_at - self._started_at)

    def get_file(self) -> str:
        """
        This function returns the file that defined the test
        :return:    the file that defined the test
        """
        return self._file

    def get_method(self) -> str:
        """
        This function returns the method that defined the test
        :return:    the method that defined the test
        """
        return self._method

    def get_started_at(self) -> float:
        """
        This function returns the time at which the test was started
        :return:    the timestamp at which the test was started
        """
        return self._started_at

    def get_status(self) -> TestStatus:
        """
        This function returns the status with which the test exited
        :return:    the test (exit) status
        """
        return self._status

    def get_stopped_at(self) -> float:
        """
        This function returns the time at which the test was stopped
        :return:    the timestamp at which the test was stopped
        """
        return self._stopped_at
