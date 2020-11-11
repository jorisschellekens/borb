import base64

from ptext.primitive.pdf_dictionary import PDFDictionary


class ASCII85Decode:
    @staticmethod
    def decode_with_parameter_dictionary(
        bytes_in: bytes, decode_params: PDFDictionary = None
    ) -> bytes:

        exceptions_to_throw = []

        # normal decode
        try:
            return base64.a85decode(bytes_in)
        except Exception as e:
            exceptions_to_throw.append(e)
            pass

        # Adobe decode
        try:
            return base64.a85decode(bytes_in, adobe=True)
        except Exception as e:
            exceptions_to_throw.append(e)
            pass

        # we should not be here
        raise exceptions_to_throw[0]
