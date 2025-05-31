#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for decoding data compressed using the Flate (zlib) compression algorithm.

The FlateDecode algorithm is commonly used in PDF files to compress streams of data, particularly
when dealing with images or other binary data. Flate compression works efficiently by finding patterns
in the input data and encoding it in a way that reduces its size. It is a form of lossless compression,
meaning the original data can be fully reconstructed after decompression.

PDF files also support predictor functions to improve the effectiveness of compression algorithms like
Flate. These functions adjust the input data before compression, making it more predictable and
improving compression ratios. The most common predictor function used in PDFs is the TIFF Predictor 2,
which is a form of adaptive prediction applied to neighboring pixels or samples.

The `FlateDecode` class handles the decompression of data compressed using the Flate algorithm,
including support for handling different prediction methods that may have been applied to the data.
"""
import typing


class FlateDecode:
    """
    A class for decoding data compressed using the Flate (zlib) compression algorithm.

    The FlateDecode algorithm is commonly used in PDF files to compress streams of data, particularly
    when dealing with images or other binary data. Flate compression works efficiently by finding patterns
    in the input data and encoding it in a way that reduces its size. It is a form of lossless compression,
    meaning the original data can be fully reconstructed after decompression.

    PDF files also support predictor functions to improve the effectiveness of compression algorithms like
    Flate. These functions adjust the input data before compression, making it more predictable and
    improving compression ratios. The most common predictor function used in PDFs is the TIFF Predictor 2,
    which is a form of adaptive prediction applied to neighboring pixels or samples.

    The `FlateDecode` class handles the decompression of data compressed using the Flate algorithm,
    including support for handling different prediction methods that may have been applied to the data.
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
        Decode data compressed using the Flate algorithm, optionally applying a predictor function based on the TIFF specification to improve compression efficiency.

        This method decompresses the input byte stream that has been compressed using Flate (zlib)
        compression. The method also supports decoding of data that was pre-processed with a predictor
        function to improve compression, commonly used in image compression (e.g., TIFF).

        The TIFF predictor functions modify the data before compression to make it more predictable,
        thus improving the compression ratio. The most commonly used predictor functions are Predictor 1
        (no prediction) and Predictor 2 (subtraction of neighboring pixel values).

        :param bytes_in:              The input byte sequence to be decompressed. It should represent Flate-compressed data.
        :param bits_per_component:    The number of bits per sample/component of the data (default is 8). This parameter affects how the data is processed after decompression.
        :param columns:               The number of columns in the data. This is relevant when applying certain predictor functions that need to know the structure of the data (default is 1).
        :param predictor:             The type of predictor function applied to the data before compression. Default is 1 (no prediction). Other possible values, such as 2, correspond to the TIFF Predictor 2.
        :return:                      The decompressed byte sequence, which may have had a predictor applied and been compressed with the Flate algorithm.
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
        import zlib

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
            import copy

            prior_row = copy.deepcopy(current_row)

        # return
        return bytes([(int(x) % 256) for x in bytes_after_predictor])
