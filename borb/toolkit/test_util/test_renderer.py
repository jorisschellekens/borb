#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class represents the interface for rendering a test.
The various methods here can be overwritten to provide a custom implementation.
"""
import typing
from unittest import TestResult

from borb.pdf.document.document import Document


class TestRenderer:
    """
    This class represents the interface for rendering a test.
    The various methods here can be overwritten to provide a custom implementation.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def build_pdf_back_cover_page(self, d: Document) -> None:
        """
        This function is called to build the (back) cover Page of the PDF
        :param d:   the PDF to which the cover page can be added
        :return:    None
        """
        return

    def build_pdf_front_cover_page(self, d: Document) -> None:
        """
        This function is called to build the (front) cover Page of the PDF
        :param d:   the PDF to which the cover page can be added
        :return:    None
        """
        return

    def build_pdf_module_page(self, d: Document, t: typing.List[TestResult]) -> None:
        """
        This function is called to build content for each typing.List[TestResult] representing a module that was tested
        :param d:   the PDF to which the cover page can be added
        :param t:   the typing.List[TestResult]  representing the module that was tested
        :return:    None
        """
        return

    def build_pdf_summary_page(self, d: Document, t: typing.List[TestResult]) -> None:
        """
        This function is called to build content representing a summary of all tests that were run
        :param d:   the PDF to which the cover page can be added
        :param t:   the typing.List[TestResult]  representing all tests that were run
        :return:    None
        """
        return
