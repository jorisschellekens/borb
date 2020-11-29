from codecs import decode

from ptext.exception.pdf_exception import PDFValueError
from ptext.io.filter.ascii85_decode import ASCII85Decode
from ptext.io.filter.flate_decode import FlateDecode
from ptext.io.filter.lzw_decode import LZWDecode
from ptext.io.filter.run_length_decode import RunLengthDecode
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_dictionary import PDFDictionary
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject


class PDFStream(PDFObject):
    """
    A stream object, like a string object, is a sequence of bytes. Furthermore, a stream may be of unlimited length,
    whereas a string shall be subject to an implementation limit. For this reason, objects with potentially large
    amounts of data, such as images and page descriptions, shall be represented as streams.
    """

    def __init__(
        self,
        stream_dictionary: PDFDictionary,
        raw_byte_array: bytes,
    ):
        super().__init__()
        self.stream_dictionary = stream_dictionary
        self.raw_byte_array = raw_byte_array

    def get_decoded_bytes(self):

        # read filters
        filter_name = PDFName("Filter")
        filters = []
        if filter_name in self.stream_dictionary:
            filters = self.stream_dictionary[filter_name]
            if not isinstance(filters, PDFArray):
                filters = [filters]

        # apply
        decode_params_name = PDFName("DecodeParms")
        transformed_bytes = self.raw_byte_array
        for filter_name in filters:
            # FLATE
            if filter_name in [PDFName("FlateDecode"), PDFName("Fl")]:
                transformed_bytes = FlateDecode.decode_with_parameter_dictionary(
                    transformed_bytes,
                    self.stream_dictionary[decode_params_name]
                    if decode_params_name in self.stream_dictionary
                    else None,
                )
                continue

            # ASCII85
            if filter_name in [PDFName("ASCII85Decode")]:
                transformed_bytes = ASCII85Decode.decode(transformed_bytes)
                continue

            # LZW
            if filter_name in [PDFName("LZWDecode")]:
                transformed_bytes = LZWDecode.decode(transformed_bytes)
                continue

            # RunLengthDecode
            if filter_name in [PDFName("RunLengthDecode")]:
                transformed_bytes = RunLengthDecode.decode(transformed_bytes)
                continue

            # unknown filter
            raise PDFValueError(
                expected_value_description="[/ASCII85Decode, /FlateDecode, /Fl, /LZWDecode, /RunLengthDecode]",
                received_value_description=str(filter_name),
            )
        # return
        return transformed_bytes

    def get_bytes(self):
        return self.raw_byte_array

    def __str__(self):
        return (
            str(self.stream_dictionary)
            + "\nstream\n"
            + decode(self.raw_byte_array, "latin-1")
            + "\nendstream\n"
        )
