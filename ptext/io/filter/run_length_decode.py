from ptext.primitive.pdf_dictionary import PDFDictionary


class RunLengthDecode:
    @staticmethod
    def decode_with_parameter_dictionary(
        bytes_in: bytes, decode_params: PDFDictionary = None
    ) -> bytes:

        bytes_out = bytearray()
        for i in range(0, len(bytes_in), 2):
            b = bytes_in[i]
            n = bytes_in[i + 1]
            for j in range(0, n):
                bytes_out.append(b)

        return bytes(bytes_out)
