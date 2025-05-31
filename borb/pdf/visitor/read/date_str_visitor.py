#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing date strings in a PDF byte stream.

`DateStrVisitor` extends `ReadVisitor` to identify and process date-formatted
string objects within a PDF, converting them into structured Python representations.
Using the visitor pattern, `DateStrVisitor` traverses PDF nodes, extracts date values
according to the PDF specification, and enables precise handling of temporal metadata
embedded in the document.
"""
import typing

from borb.pdf.primitives import PDFType, datestr
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class DateStrVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing date strings in a PDF byte stream.

    `DateStrVisitor` extends `ReadVisitor` to identify and process date-formatted
    string objects within a PDF, converting them into structured Python representations.
    Using the visitor pattern, `DateStrVisitor` traverses PDF nodes, extracts date values
    according to the PDF specification, and enables precise handling of temporal metadata
    embedded in the document.
    """

    __STR_CLOSE_BRACKET = b")"
    __STR_OPEN_BRACKET = b"("

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
    def visit(
        self, node: typing.Union[int, PDFType]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        if not isinstance(node, int):
            return None
        if self.get_bytes()[node : node + 1] != DateStrVisitor.__STR_OPEN_BRACKET:
            return None

        # "D:20250427010437+00'00'"

        # D:
        i: int = node
        j: int = i + 1
        if (
            self.get_bytes()[j : j + 1] == b"D"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] == b":"
        ):
            j += 2

        # <yyyy><mm><dd><hh><mm><ss>
        year: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
            and (j + 2) < len(self.get_bytes())
            and self.get_bytes()[j + 2 : j + 3] in b"0123456789"
            and (j + 3) < len(self.get_bytes())
            and self.get_bytes()[j + 3 : j + 4] in b"0123456789"
        ):
            year = int(self.get_bytes()[j : j + 4].decode("latin1"))
            j += 4

        month: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            month = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if month is None or month < 1 or month > 12:
            return None

        day: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            day = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if day is None or day < 1 or day > 31:
            return None

        hour: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            hour = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if hour is None or hour < 1 or hour > 24:
            return None

        minute: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            minute = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if minute is None or minute > 59:
            return None

        second: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            second = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if second is None or second > 59:
            return None

        if self.get_bytes()[j : j + 1] == DateStrVisitor.__STR_CLOSE_BRACKET:
            return datestr(self.get_bytes()[i:j]), j + 1

        if self.get_bytes()[j : j + 1] in b"+-":
            j += 1

        hour_timezone: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            hour_timezone = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if hour_timezone is None or hour_timezone > 59:
            return None

        if self.get_bytes()[j : j + 1] in b"'":
            j += 1
        else:
            return None

        second_timezone: typing.Optional[int] = None
        if (
            self.get_bytes()[j : j + 1] in b"0123456789"
            and (j + 1) < len(self.get_bytes())
            and self.get_bytes()[j + 1 : j + 2] in b"0123456789"
        ):
            second_timezone = int(self.get_bytes()[j : j + 2].decode("latin1"))
            j += 2
        if second_timezone is None or second_timezone > 59:
            return None

        if self.get_bytes()[j : j + 1] in b"'":
            j += 1
        else:
            return None

        if self.get_bytes()[j : j + 1] == DateStrVisitor.__STR_CLOSE_BRACKET:
            return datestr(self.get_bytes()[i + 1 : j].decode("latin1")), j + 1

        return None
