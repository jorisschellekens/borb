#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility class for parsing specific byte patterns in PDF files.

The `PDFBytes` class provides static methods to search for specific keywords and
markers within a PDF byte stream, such as `startxref`, `%%EOF`, and the start of
the `PDF` keyword. These markers are critical for understanding the structure of
PDF files and are often needed for parsing or verifying PDF content.

Each method allows for optional specification of a search range using `start` and
`end` parameters, facilitating efficient targeted searches within the byte stream.
By supporting both forward and backward searches, `PDFBytes` enables precise
location of PDF-specific keywords, such as locating the end-of-file marker or
header indicator, which are important for tasks like validation, content extraction,
and structural analysis.
"""
import typing


class PDFBytes:
    """
    Utility class for parsing specific byte patterns in PDF files.

    The `PDFBytes` class provides static methods to search for specific keywords and
    markers within a PDF byte stream, such as `startxref`, `%%EOF`, and the start of
    the `PDF` keyword. These markers are critical for understanding the structure of
    PDF files and are often needed for parsing or verifying PDF content.

    Each method allows for optional specification of a search range using `start` and
    `end` parameters, facilitating efficient targeted searches within the byte stream.
    By supporting both forward and backward searches, `PDFBytes` enables precise
    location of PDF-specific keywords, such as locating the end-of-file marker or
    header indicator, which are important for tasks like validation, content extraction,
    and structural analysis.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __find_next(
        look_for_bytes: typing.List[bytes],
        look_in_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ) -> int:
        start = start or 0
        end = end or (start + 1024)
        assert start >= 0
        assert end >= 0
        assert end > start
        if len(look_for_bytes) == 1:
            return look_in_bytes.find(
                look_for_bytes[0], start, min(end, len(look_in_bytes))
            )
        else:
            look_for_bytes_sorted: typing.List[bytes] = sorted(
                look_for_bytes, key=lambda x: len(x), reverse=True
            )
            earliest: typing.Optional[int] = None
            for lfb in look_for_bytes_sorted:
                i: int = look_in_bytes.find(lfb, start, min(end, len(look_in_bytes)))
                if i == -1:
                    continue
                if earliest is None or i < earliest:
                    earliest = i
            return earliest or -1

    @staticmethod
    def __find_previous(
        look_for_bytes: typing.List[bytes],
        look_in_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ) -> int:
        start = start or 0
        end = end or (start - 1024)
        assert start >= 0
        assert end >= 0
        assert end < start
        if len(look_for_bytes) == 1:
            return look_in_bytes.rfind(
                look_for_bytes[0], end, min(start, len(look_in_bytes))
            )
        else:
            look_for_bytes_sorted: typing.List[bytes] = sorted(
                look_for_bytes, key=lambda x: len(x), reverse=True
            )
            latest: typing.Optional[int] = None
            for lfb in look_for_bytes_sorted:
                i: int = look_in_bytes.rfind(lfb, 0, end)
                if i == -1:
                    continue
                if latest is None or i > latest:
                    latest = i
            return latest or -1

    #
    # PUBLIC
    #

    @staticmethod
    def next_integer(
        pdf_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ):
        """
        Search for the next integer in a PDF byte stream.

        This method scans through the specified section of `pdf_bytes` to locate
        the next integer value, starting from the position defined by the `start`
        parameter. The integer is identified by its byte representation in the PDF
        file. The search can be restricted to a specific range using the `start`
        and `end` parameters.

        :param pdf_bytes: The byte sequence representing the PDF file.
        :param start: An optional integer specifying the starting position of the search range. Defaults to the beginning of `pdf_bytes` if not provided.
        :param end: An optional integer specifying the end position of the search range. Defaults to the end of `pdf_bytes` if not provided.
        :return: The byte index position of the first occurrence of an integer within the defined range, or -1 if no integer is found.
        """
        start = start or 0
        end = end or (start + 1024)
        i: int = start
        while i < min(end, len(pdf_bytes)) and pdf_bytes[i] not in [
            x[0] for x in [b"0", b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9"]
        ]:
            i += 1
        if i < min(end, len(pdf_bytes)) and pdf_bytes[i] in [
            x[0] for x in [b"0", b"1", b"2", b"3", b"4", b"5", b"6", b"7", b"8", b"9"]
        ]:
            return i
        return -1

    @staticmethod
    def next_newline(
        pdf_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ):
        r"""
        Search for the next occurrence of a newline character (`\\n` or `\\r\\n`) in a PDF byte stream.

        This method scans through the specified section of `pdf_bytes` to locate the
        first occurrence of a newline character sequence, allowing for identification
        of line boundaries within the PDF's byte data. Users can define the search range
        with the optional `start` and `end` parameters.

        :param pdf_bytes: The byte sequence representing the PDF file.
        :param start: An optional integer specifying the starting position of the search range. Defaults to the beginning of `pdf_bytes` if not provided.
        :param end: An optional integer specifying the end position of the search range. Defaults to the end of `pdf_bytes` if not provided.
        :return: The byte index position of the next newline character sequence (`\\n` or `\\r\\n`) within the defined range, or -1 if no newline is found.
        """
        return PDFBytes.__find_next(
            look_for_bytes=[b"\n", b"\n\r", b"\r\n", b"\r"],
            look_in_bytes=pdf_bytes,
            start=start,
            end=end,
        )

    @staticmethod
    def next_space(
        pdf_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ) -> int:
        """
        Search for the next occurrence of a space character in a PDF byte stream.

        This method scans through the specified section of `pdf_bytes` to locate
        the first occurrence of a space character (`' '`) within the defined range.
        The search can be restricted to a specific range using the `start` and
        `end` parameters.

        :param pdf_bytes: The byte sequence representing the PDF file.
        :param start: An optional integer specifying the starting position of the search range. Defaults to the beginning of `pdf_bytes` if not provided.
        :param end: An optional integer specifying the end position of the search range. Defaults to the end of `pdf_bytes` if not provided.
        :return: The byte index position of the first occurrence of a space character within the defined range, or -1 if no space character is found.
        """
        return PDFBytes.__find_next(
            look_for_bytes=[b" "], look_in_bytes=pdf_bytes, start=start, end=end
        )

    @staticmethod
    def next_start_of_dictionary(
        pdf_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ) -> int:
        """
        Search for the next occurrence of a dictionary in a PDF byte stream.

        This method scans through the specified section of `pdf_bytes` to locate
        the next dictionary, marked by the `<<` starting delimiter. The search
        can be restricted to a specific range using the `start` and `end` parameters.

        :param pdf_bytes: The byte sequence representing the PDF file.
        :param start: An optional integer specifying the starting position of the search range. Defaults to the beginning of `pdf_bytes` if not provided.
        :param end: An optional integer specifying the end position of the search range. Defaults to the end of `pdf_bytes` if not provided.
        :return: The byte index position of the first occurrence of a dictionary (`<<`) within the defined range, or -1 if no dictionary is found.
        """
        return PDFBytes.__find_next(
            look_for_bytes=[b"<<"], look_in_bytes=pdf_bytes, start=start, end=end
        )

    @staticmethod
    def next_start_of_pdf_keyword(
        pdf_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ) -> int:
        """
        Search for the next occurrence of the "PDF" keyword in a PDF byte stream.

        This method scans through the specified section of `pdf_bytes` to locate
        the first occurrence of the "PDF" keyword, which commonly appears in the
        header of PDF files (e.g., `%PDF-`). It can assist in identifying the start
        of the PDF content or verifying the file structure. The search range can be
        specified with optional `start` and `end` parameters.

        :param pdf_bytes: The byte sequence representing the PDF file.
        :param start: An optional integer specifying the starting position of the search range. Defaults to the beginning of `pdf_bytes` if not provided.
        :param end: An optional integer specifying the end position of the search range. Defaults to the end of `pdf_bytes` if not provided.
        :return: The byte index position of the first occurrence of "PDF" within the defined range, or -1 if "PDF" is not found.
        """
        return PDFBytes.__find_next(
            look_for_bytes=[b"%PDF"], look_in_bytes=pdf_bytes, start=start, end=end
        )

    @staticmethod
    def previous_eof_keyword(
        pdf_bytes: bytes,
        start: typing.Optional[int] = None,
        end: typing.Optional[int] = None,
    ) -> int:
        """
        Search backward for the previous occurrence of the "%%EOF" keyword in a PDF byte stream.

        This method scans backward within a specified range of `pdf_bytes` to locate the last
        occurrence of the "%%EOF" keyword, which signifies the end of a PDF file. This search
        can be used to verify the file's structure or identify the end marker within a PDF
        document. The search range can be restricted using optional `start` and `end` parameters.

        :param pdf_bytes: The byte sequence representing the PDF file.
        :param start: An optional integer specifying the starting position to search backward from. Defaults to the end of `pdf_bytes` if not provided.
        :param end: An optional integer specifying the lower limit of the search range. Defaults to 1024 bytes before the `start` position if not provided.
        :return: The byte index position of the last occurrence of "%%EOF" within the defined range, or -1 if "%%EOF" is not found.
        """
        return PDFBytes.__find_previous(
            look_for_bytes=[b"%%EOF"], look_in_bytes=pdf_bytes, start=start, end=end
        )
