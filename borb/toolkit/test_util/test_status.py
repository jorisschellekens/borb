#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This enum.Enum represents the ways in which a test can be concluded.
"""
import enum


class TestStatus(enum.Enum):
    """
    This enum.Enum represents the ways in which a test can be concluded.
    """

    ERROR = 1
    EXPECTED_FAILURE = 2
    FAILURE = 3
    SKIP = 4
    SUCCESS = 5
    UNEXPECTED_SUCCESS = 6
