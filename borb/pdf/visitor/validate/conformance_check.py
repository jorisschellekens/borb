#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a single conformance check against a specific clause in a PDF specification.

This class encapsulates all necessary metadata and logic required to verify whether
a given object conforms to a specific requirement in the PDF standard.
"""
import typing

from borb.pdf.conformance import Conformance


class ConformanceCheck:
    """
    Represents a single conformance check against a specific clause in a PDF specification.

    This class encapsulates all necessary metadata and logic required to verify whether
    a given object conforms to a specific requirement in the PDF standard.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        clause: str,
        conformance: typing.List[Conformance],
        description: str,
        lambda_function_to_check_object: typing.Callable[[typing.Any], bool],
        specification: str,
        test_number: int,
    ):
        """
        Initialize a ConformanceCheck instance.

        :param clause: Clause identifier from the specification.
        :param conformance: List of applicable conformance levels (e.g., ["PDF/A-1b", "PDF/UA"]).
        :param description: Description of the validation check.
        :param lambda_function_to_check_object: Callable that returns True if the object violates the clause.
        :param specification: Name or reference of the specification (e.g., "ISO 19005-1").
        :param test_number: Numerical identifier for this test.
        """
        self.__clause: str = clause
        self.__conformance: typing.List[Conformance] = conformance
        self.__description: str = description
        self.__lambda_function_to_check_object: typing.Callable[[typing.Any], bool] = (
            lambda_function_to_check_object
        )
        self.__specification: str = specification
        self.__test_number = test_number

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def check_whether_object_violates_clause(self, obj: typing.Any) -> bool:
        """
        Evaluate whether the given object violates the clause.

        :param obj: The object to evaluate.
        :return: True if the object violates the clause, False otherwise.
        """
        return self.__lambda_function_to_check_object(obj)

    def get_clause(self) -> str:
        """
        Get the clause identifier from the specification.

        :return: The clause identifier.
        """
        return self.__clause

    def get_conformance(self) -> typing.List[Conformance]:
        """
        Get the list of applicable conformance levels.

        :return: List of conformance levels.
        """
        return self.__conformance

    def get_description(self) -> str:
        """
        Get the human-readable description of the check.

        :return: Description of the validation logic.
        """
        return self.__description

    def get_specification(self) -> str:
        """
        Get the name or reference of the specification.

        :return: Specification name.
        """
        return self.__specification

    def get_test_number(self):
        """
        Get the numerical identifier for this test.

        :return: Test number.
        """
        return self.__test_number
