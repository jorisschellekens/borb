#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for applying ASCII85 decoding to data in a PDF document.

The `ASCII85Decode` class implements the ASCII85 (also known as Base85) decoding scheme,
which is a form of binary-to-text encoding commonly used in PDF files. This method allows
the decoding of ASCII-encoded data that was originally compressed or encoded in ASCII85
format. It converts the ASCII85-encoded string back into the original binary data.

ASCII85 decoding is used in PDFs for more efficient storage of binary data, such as images
or streams, by representing binary information as a set of ASCII characters.
"""


class ASCII85Decode:
    """
    A class for applying ASCII85 decoding to data in a PDF document.

    The `ASCII85Decode` class implements the ASCII85 (also known as Base85) decoding scheme,
    which is a form of binary-to-text encoding commonly used in PDF files. This method allows
    the decoding of ASCII-encoded data that was originally compressed or encoded in ASCII85
    format. It converts the ASCII85-encoded string back into the original binary data.

    ASCII85 decoding is used in PDFs for more efficient storage of binary data, such as images
    or streams, by representing binary information as a set of ASCII characters.
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

    @staticmethod
    def decode(bytes_in: bytes) -> bytes:
        """
        Decode data encoded in ASCII85 (Base85) representation.

        This method takes an input byte sequence that has been encoded using ASCII85
        encoding and decodes it back into the original binary data. ASCII85 is a method of
        representing binary data using printable ASCII characters, and is commonly used
        in PDF files for compressing or encoding binary data such as images or streams.

        :param bytes_in: The byte sequence that is encoded in ASCII85 format.
        :return: The decoded binary data as a byte sequence.
        """
        exceptions_to_throw = []

        # trivial case
        if len(bytes_in) == 0:
            return bytes_in

        # trimming
        if bytes_in[-1] == 10 and bytes_in[-2] == 13:
            bytes_in = bytes_in[0:-2]
        if bytes_in[-1] == 10:
            bytes_in = bytes_in[0:-1]
        if bytes_in[-1] == 13:
            bytes_in = bytes_in[0:-1]

        # normal decode
        import base64

        try:
            return base64.a85decode(bytes_in)
        except Exception as e:
            exceptions_to_throw.append(e)
            pass

        # adobe decode
        try:
            return base64.a85decode(bytes_in, adobe=True)
        except Exception as e:
            exceptions_to_throw.append(e)
            pass

        # we should not be here
        raise exceptions_to_throw[0]
