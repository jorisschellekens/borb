#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decodes data encoded in an ASCII base-85 representation,
reproducing the original binary data.
"""

import base64


class ASCII85Decode:
    """
    Decodes data encoded in an ASCII base-85 representation,
    reproducing the original binary data.
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
        Decodes data encoded in an ASCII base-85 representation
        :param bytes_in:    the input bytes
        :return:            the output bytes
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
