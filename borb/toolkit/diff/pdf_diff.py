#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class was meant to perform a dictionary/array level comparison of PDF documents.
    It makes it a lot easier to debug problems.
"""
import typing

from borb.io.filter.stream_decode_util import decode_stream
from borb.io.read.types import Decimal, Dictionary, List, Name, Stream
from borb.pdf.document.document import Document


class PDFDiff:
    """
    This class was meant to perform a dictionary/array level comparison of PDF documents.
    It makes it a lot easier to debug problems.
    """

    def __init__(self, pdf_a: Document, pdf_b: Document):
        self._document_a: Document = pdf_a
        self._document_b: Document = pdf_b
        self._already_compared: typing.List[int] = []
        self._errors: typing.List[str] = []

    def compare(self) -> None:
        """
        This method compares the given PDF documents, logging any differences between them.
        """
        self._compare(self._document_a, self._document_b, "", "")

    @staticmethod
    def _get_reference_or_none(obj) -> str:
        try:
            if obj.get_reference() is not None:
                return "(%d 0 R)" % obj.get_reference().object_number
        except:
            pass
        return ""

    def _log_difference(self, error_msg: str) -> None:
        print(error_msg)
        self._errors.append(error_msg)

    def _compare(self, a, b, path_to_a, path_to_b) -> None:

        if id(a) in self._already_compared:
            return
        if id(b) in self._already_compared:
            return
        self._already_compared.append(id(a))
        self._already_compared.append(id(b))

        # check type
        if a.__class__.__name__ != b.__class__.__name__:
            self._log_difference(
                "Class mismatch : %s %s <--> %s %s"
                % (path_to_a, a.__class__.__name__, path_to_b, b.__class__.__name__)
            )

        if isinstance(a, Name):
            if str(a) != str(b):
                self._log_difference(
                    "Name mismatch : %s %s <--> %s %s"
                    % (path_to_a, str(a), path_to_b, str(b))
                )
            return

        if isinstance(a, Decimal):
            if int(a) != int(b):
                self._log_difference(
                    "Value mismatch : %s %s <--> %s %s"
                    % (path_to_a, str(a), path_to_b, str(b))
                )

        # get references if they exist
        ref_a = PDFDiff._get_reference_or_none(a)
        ref_b = PDFDiff._get_reference_or_none(a)

        # compare streams
        if isinstance(a, Stream):
            decode_stream(a)
            decode_stream(b)
            if "DecodedBytes" not in a:
                self._log_difference("Unable to decode Stream %s" % (path_to_a + ref_a))
            if "DecodedBytes" not in b:
                self._log_difference("Unable to decode Stream %s" % (path_to_b + ref_b))
            dba: bytes = a["DecodedBytes"]
            dbb: bytes = b["DecodedBytes"]
            if len(dba) != len(dbb):
                self._errors.append(
                    "Stream Length mismatch : %s %d <--> %s %d"
                    % (path_to_a + ref_a, len(a), path_to_b + ref_b, len(b))
                )
            else:
                for i in range(0, len(dba)):
                    if dba[i] != dbb[i]:
                        self._errors.append(
                            "Stream content mismatch : %s %d <--> %s %d"
                            % (path_to_a + ref_a, i, path_to_b + ref_b, i)
                        )

        # compare dictionary
        if isinstance(a, Dictionary):
            for k, v in a.items():
                if k == "ID":
                    continue
                if k == "Bytes":
                    continue
                if k == "DecodedBytes":
                    continue
                if isinstance(a, Stream) and k == "Length":
                    continue
                if k not in b:
                    self._log_difference(
                        "Key absent/present mismatch : %s %s <--> %s %s"
                        % (path_to_a + ref_a, str(k), path_to_b + ref_b, None)
                    )
                    continue
                self._compare(
                    a[k],
                    b[k],
                    path_to_a + "/" + str(k) + ref_a,
                    path_to_b + "/" + str(k) + ref_b,
                )
            return

        # compare array
        if isinstance(a, List):
            if len(a) != len(b):
                self._errors.append(
                    "Array Length mismatch : %s %d <--> %s %d"
                    % (path_to_a + ref_a, len(a), path_to_b + ref_b, len(b))
                )
            for i in range(0, min(len(a), len(b))):
                self._compare(
                    a[i],
                    b[i],
                    path_to_a + ref_a + "/" + str(i),
                    path_to_b + ref_b + "/" + str(i),
                )
            return
