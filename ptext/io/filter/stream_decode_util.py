import typing

from ptext.exception.pdf_exception import PDFValueError
from ptext.io.filter.ascii85_decode import ASCII85Decode
from ptext.io.filter.flate_decode import FlateDecode
from ptext.io.filter.lzw_decode import LZWDecode
from ptext.io.filter.run_length_decode import RunLengthDecode
from ptext.io.read_transform.types import Stream, List, Decimal, Dictionary, Name


def decode_stream(s: Stream) -> Stream:

    assert isinstance(s, Stream)
    assert "Bytes" in s

    # determine filter(s) to apply
    filters: typing.List[str] = []
    if "Filter" in s:
        if isinstance(s["Filter"], List):
            filters = s["Filter"]
        else:
            filters = [s["Filter"]]

    decode_params: typing.List[Dictionary] = []
    if "DecodeParms" in s:
        if isinstance(s["DecodeParms"], List):
            decode_params = s["DecodeParms"]
        else:
            assert s["DecodeParms"] is not None
            assert isinstance(s["DecodeParms"], Dictionary)
            decode_params = [s["DecodeParms"]]
    else:
        decode_params = [Dictionary() for x in range(0, len(filters))]

    # apply filter(s)
    transformed_bytes = s["Bytes"]
    for filter_index, filter_name in enumerate(filters):
        # FLATE
        if filter_name in ["FlateDecode", "Fl"]:
            transformed_bytes = FlateDecode.decode(
                bytes_in=transformed_bytes,
                columns=int(decode_params[filter_index].get("Columns", Decimal(1))),
                predictor=int(decode_params[filter_index].get("Predictor", Decimal(1))),
                bits_per_component=int(
                    decode_params[filter_index].get("BitsPerComponent", Decimal(8))
                ),
            )
            continue

        # ASCII85
        if filter_name in ["ASCII85Decode"]:
            transformed_bytes = ASCII85Decode.decode(transformed_bytes)
            continue

        # LZW
        if filter_name in ["LZWDecode"]:
            transformed_bytes = LZWDecode.decode(transformed_bytes)
            continue

        # RunLengthDecode
        if filter_name in ["RunLengthDecode"]:
            transformed_bytes = RunLengthDecode.decode(transformed_bytes)
            continue

        # unknown filter
        raise PDFValueError(
            expected_value_description="[/ASCII85Decode, /FlateDecode, /Fl, /LZWDecode, /RunLengthDecode]",
            received_value_description=str(filter_name),
        )

    # set DecodedBytes
    s[Name("DecodedBytes")] = transformed_bytes

    # set Type if not yet set
    if "Type" not in s:
        s[Name("Type")] = Name("Stream")

    # return
    return s
