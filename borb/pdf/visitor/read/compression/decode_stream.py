#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF Stream Decoder Module.

This module provides functionality for decoding compressed PDF `stream` objects,
applying the appropriate decompression filters specified in each stream's `Filter` entry.

PDF streams may use various encoding methods to reduce file size, including but not
limited to:
- **FlateDecode** (zlib or DEFLATE-based compression)
- **ASCII85Decode** (ASCII base-85 encoding)
- **LZWDecode** (LZW compression, used in image data and other highly repetitive content)
- **RunLengthDecode** (Run-length encoding, suitable for monochrome images or data with long runs of single-byte values)

The `decode_stream` function in this module detects and applies these filters, allowing
compressed data within the PDF to be decoded for processing, rendering, or other uses.
If multiple filters are applied to a stream, `decode_stream` processes them sequentially
in the order they are listed.
"""

import typing

from borb.pdf.primitives import stream, name
from borb.pdf.visitor.read.compression.ascii85_decode import ASCII85Decode
from borb.pdf.visitor.read.compression.flate_decode import FlateDecode
from borb.pdf.visitor.read.compression.lzw_decode import LZWDecode
from borb.pdf.visitor.read.compression.run_length_decode import RunLengthDecode


#
# CONSTRUCTOR
#

#
# PRIVATE
#

#
# PUBLIC
#


def decode_stream(s: stream) -> stream:
    """
    Decode a PDF `stream` object, applying compression filters specified in the stream's `Filter` entry.

    This function takes a PDF `stream` object that may be encoded with various
    compression algorithms (such as Flate, ASCII85, LZW, or Run-Length encoding),
    decodes the `Bytes` content within the stream, and stores the resulting uncompressed
    content under the `DecodedBytes` entry in the stream dictionary.

    If the stream is already decoded (has a `DecodedBytes` entry), the function returns
    immediately without further processing.

    :param s:   The input `stream` object, containing raw (potentially compressed)
                byte data in its `Bytes` entry and metadata in `Filter` and
                `DecodeParms` entries for specifying the encoding filters
                and parameters.
    :return:    The input `stream`, modified to include decoded data in the `DecodedBytes`
                entry, ready for uncompressed access.
    """
    # fmt: off
    assert isinstance(s, stream), "decode_stream only works on Stream objects"
    assert ("Bytes" in s), "decode_stream only works on Stream objects with a `Bytes` key."
    # fmt: on

    # IF stream already has /DecodedBytes
    # THEN return stream
    if "DecodedBytes" in s:
        return s

    # determine filter(s) to apply
    filters: typing.List[str] = []
    if "Filter" in s:
        if isinstance(s["Filter"], list):
            filters = s["Filter"]
        else:
            filters = [s["Filter"]]

    decode_params: typing.List[typing.Dict] = []
    if "DecodeParms" in s:
        if isinstance(s["DecodeParms"], list) and s["DecodeParms"] is not None:
            decode_params = s["DecodeParms"]
            decode_params = [x or dict() for x in decode_params]
        if isinstance(s["DecodeParms"], dict) and s["DecodeParms"] is not None:
            decode_params = [s["DecodeParms"]]
    else:
        decode_params = [{} for x in range(0, len(filters))]

    # apply filter(s)
    transformed_bytes = s["Bytes"]
    for filter_index, filter_name in enumerate(filters):
        # FLATE
        if filter_name in ["FlateDecode", "Fl"]:
            transformed_bytes = FlateDecode.decode(
                bytes_in=transformed_bytes,
                columns=int(decode_params[filter_index].get("Columns", 1)),
                predictor=int(decode_params[filter_index].get("Predictor", 1)),
                bits_per_component=int(
                    decode_params[filter_index].get("BitsPerComponent", 8)
                ),
            )
            continue

        # ASCII85
        if filter_name in ["ASCII85Decode"]:
            transformed_bytes = ASCII85Decode.decode(transformed_bytes)
            continue

        # LZW
        if filter_name in ["LZWDecode"]:
            transformed_bytes = LZWDecode().decode(transformed_bytes)
            continue

        # RunLengthDecode
        if filter_name in ["RunLengthDecode"]:
            transformed_bytes = RunLengthDecode.decode(transformed_bytes)
            continue

        # unknown filter
        assert False, "Unknown /Filter %s" % filter_name

    # set DecodedBytes
    s[name("DecodedBytes")] = transformed_bytes

    # return
    return s
