#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LZW and Flate encoding compress more compactly if their input data is highly predictable.
One way of increasing the predictability of many continuous-tone sampled images is to replace each sample with the
difference between that sample and a predictor function applied to earlier neighboring samples.
If the predictor function works well, the postprediction data clusters toward 0.
PDF supports two groups of Predictor functions.
The first, the TIFF group, consists of the single function that is Predictor 2 in the TIFF 6.0 specification.
"""
import copy
import typing
import zlib


class FlateDecode:
    """
    LZW and Flate encoding compress more compactly if their input data is highly predictable.
    One way of increasing the predictability of many continuous-tone sampled images is to replace each sample with the
    difference between that sample and a predictor function applied to earlier neighboring samples.
    If the predictor function works well, the postprediction data clusters toward 0.
    PDF supports two groups of Predictor functions.
    The first, the TIFF group, consists of the single function that is Predictor 2 in the TIFF 6.0 specification.
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
    def decode(
        bytes_in: bytes,
        bits_per_component: int = 8,
        columns: int = 1,
        predictor: int = 1,
    ) -> bytes:
        """
        LZW and Flate encoding compress more compactly if their input data is highly predictable.
        One way of increasing the predictability of many continuous-tone sampled images is to replace each sample with the
        difference between that sample and a predictor function applied to earlier neighboring samples.
        If the predictor function works well, the postprediction data clusters toward 0.
        PDF supports two groups of Predictor functions.
        The first, the TIFF group, consists of the single function that is Predictor 2 in the TIFF 6.0 specification.
        :param bytes_in:            the input bytes
        :param bits_per_component:  the number of bits per component
        :param columns:             the number of columns
        :param predictor:           which predictor to use
        :return:                    the output bytes
        """

        # trivial case
        if len(bytes_in) == 0:
            return bytes_in

        # check /Predictor
        # fmt: off
        assert predictor in [1, 2, 10, 11, 12, 13, 14, 15,], "Illegal argument exception. predictor must be in [1, 2, 10, 11, 12, 13, 14, 15]."
        # fmt: on

        # check /BitsPerComponent
        # fmt: off
        assert bits_per_component in [1, 2, 4, 8], "Illegal argument exception. bits_per_component must be in [1, 2, 4, 8]."
        # fmt: on

        # initial transform
        bytes_after_zlib = zlib.decompress(bytes_in, bufsize=4092)

        # LZW and Flate encoding compress more compactly if their input data is highly predictable. One way of
        # increasing the predictability of many continuous-tone sampled images is to replace each sample with the
        # difference between that sample and a predictor function applied to earlier neighboring samples. If the predictor
        # function works well, the postprediction data clusters toward 0.
        # PDF supports two groups of Predictor functions. The first, the TIFF group, consists of the single function that is
        # Predictor 2 in the TIFF 6.0 specification.

        # check predictor
        if predictor == 1:
            return bytes_after_zlib

        # set up everything to do PNG prediction
        bytes_per_row: int = int((columns * bits_per_component + 7) / 8)
        bytes_per_pixel = int(bits_per_component / 8)

        current_row: typing.List[int] = [0 for _ in range(0, bytes_per_row)]
        prior_row: typing.List[int] = [0 for _ in range(0, bytes_per_row)]
        number_of_rows = int(len(bytes_after_zlib) / bytes_per_row)

        # easy case
        bytes_after_predictor = [int(x) for x in bytes_after_zlib]
        if predictor == 2:
            if bits_per_component == 8:
                for row in range(0, number_of_rows):
                    row_start_index = row * bytes_per_row
                    for col in range(1, bytes_per_row):
                        bytes_after_predictor[row_start_index + col] = (
                            bytes_after_predictor[row_start_index + col]
                            + bytes_after_predictor[row_start_index + col - 1]
                        ) % 256
                return bytes([(int(x) % 256) for x in bytes_after_predictor])

        # harder cases
        bytes_after_predictor = []
        pos = 0
        while pos + bytes_per_row <= len(bytes_after_zlib):
            # Read the filter type byte and a row of data
            filter_type = bytes_after_zlib[pos]
            pos += 1

            current_row = [x for x in bytes_after_zlib[pos : pos + bytes_per_row]]
            pos += bytes_per_row

            # PNG_FILTER_NONE
            if filter_type == 0:
                # DO NOTHING
                pass

            # PNG_FILTER_SUB
            # Predicts the same as the sample to the left
            if filter_type == 1:
                for i in range(bytes_per_pixel, bytes_per_row):
                    current_row[i] = (
                        current_row[i] + current_row[i - bytes_per_pixel]
                    ) % 256

            # PNG_FILTER_UP
            # Predicts the same as the sample above
            if filter_type == 2:
                for i in range(0, bytes_per_row):
                    current_row[i] = (current_row[i] + prior_row[i]) % 256

            # PNG_FILTER_AVERAGE
            # Predicts the average of the sample to the left and the
            # sample above
            if filter_type == 3:
                for i in range(0, bytes_per_pixel):
                    current_row[i] += int(prior_row[i] / 2)

                for i in range(bytes_per_pixel, bytes_per_row):
                    current_row[i] += (int)(
                        (current_row[i - bytes_per_pixel] + prior_row[i]) / 2
                    )
                    current_row[i] %= 256

            # PNG_FILTER_PAETH
            if filter_type == 4:
                for i in range(0, bytes_per_pixel):
                    current_row[i] += prior_row[i]

                for i in range(bytes_per_pixel, bytes_per_row):
                    a = current_row[i - bytes_per_pixel]
                    b = prior_row[i]
                    c = prior_row[i - bytes_per_pixel]

                    p = a + b - c
                    pa = abs(p - a)
                    pb = abs(p - b)
                    pc = abs(p - c)

                    ret = 0
                    if pa <= pb and pa <= pc:
                        ret = a
                    elif pb <= pc:
                        ret = b
                    else:
                        ret = c

                    current_row[i] = (current_row[i] + ret) % 256

            # write current row
            for i in range(0, len(current_row)):
                bytes_after_predictor.append(current_row[i])

            # Swap curr and prior
            prior_row = copy.deepcopy(current_row)

        # return
        return bytes([(int(x) % 256) for x in bytes_after_predictor])
